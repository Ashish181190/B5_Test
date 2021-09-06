from django.contrib.auth.models import User
from django.db import models
from django.utils.text import Truncator


class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)

    class Meta:
        db_table = 'board'

    def __str__(self):
        return self.name
    
    def get_posts_count(self):
        return Post.objects.filter(topic__board= self).count()

    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by('-created_at').first()


class Topic(models.Model):
    subject = models.CharField(max_length=200)
    last_updated = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, related_name= 'topics', on_delete= models.CASCADE)
    starter = models.ForeignKey(User, related_name='topics', on_delete= models.CASCADE)
    views = models.PositiveIntegerField(default=0)
    
    class Meta:
        db_table = 'topic'

    def __str__(self):
        return self.subject

class Post(models.Model):
    message = models.TextField(max_length=5000)
    topic = models.ForeignKey(Topic, related_name='posts', on_delete= models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='posts', on_delete= models.CASCADE)
    upated_by = models.ForeignKey(User, related_name='+', null=True, on_delete= models.CASCADE)

    class Meta:
        db_table = "post"

    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(30)
