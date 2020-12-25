from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Blog(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=1000)
    publish_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.BigIntegerField(default=0)

    def __str__(self):
        return self.title
    
    # This code redirects to 'post/<post_id>/' after successful creation of a Post
    def get_absolute_url(self):
        return reverse('view_post', kwargs={'pk': self.pk})


class Likes_Table(models.Model):
    '''Table to store which User has Liked/Disliked which Post. Used to highlight Up/Down carets when a particular user is logged in'''
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Blog, on_delete=models.CASCADE)
    # Denotes the Like status -> 1: User has Liked Post  0: User has Disliked Post
    like_status_id = models.BooleanField()

    
        