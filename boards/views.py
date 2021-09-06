import django
from django.core.checks import messages
from django.db.models import Count
from django.http import Http404, HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from myproject.settings import ROOT_URLCONF
from django.contrib.auth.decorators import login_required

from boards.forms import NewTopicForm, PostForm

# Create your views here.
from .models import Board, Post, Topic, User


def home(request):
    " Go to home page"
    boards = Board.objects.all()
    return render(request, "home.html", {'boards': boards})

@login_required
def board_topics(request, pk):
    " Go to topics.html file/page "
    try:
        board = Board.objects.get(pk=pk)
    except Board.DoesNotExist:
        raise Http404
    return render(request, 'topics.html', {'board': board})

@login_required
def new_topic(request, pk):
    ' Creating new topic '
    board = get_object_or_404(Board, pk=pk)
    # print(request.user.id)
    user = request.user #User.objects.first()
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user
            )
            return redirect('topic_posts', pk= board.pk, topic_pk = topic.pk)

    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})


def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk= topic_pk)
    return render(request, 'topic_posts.html', {'topic': topic})

@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk = pk, pk = topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topic_posts', pk=pk, topic_pk= topic_pk)

    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic':topic, 'form': form})


def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    topics = board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
    return render(request, 'topics.html', {'board': board, 'topics': topics})


def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk= pk, pk=topic_pk)
    topic.views += 1
    topic.save()
    return render(request, 'topic_posts.html', {'topic': topic})