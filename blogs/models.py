from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Blog(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=10000)
    publish_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.BigIntegerField(default=0)
    image = models.ImageField(upload_to='posts_images', blank=True, null=True)
    views = models.BigIntegerField(default=0)

    def __str__(self):
        return self.title

    # This code redirects to 'post/<post_id>/' after successful creation of a Post
    def get_absolute_url(self):
        return reverse('view_post', kwargs={'pk': self.pk})

    # Function to return the Number of comments for this post

    def number_of_comments(self):
        return Blog_comments.objects.filter(blogpost=self).count()


class Likes_Table(models.Model):
    '''Table to store which User has Liked/Disliked which Post. Used to highlight Up/Down carets when a particular user is logged in'''
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Blog, on_delete=models.CASCADE)
    # Denotes the Like status -> 1: User has Liked Post  0: User has Disliked Post
    like_status_id = models.BooleanField()


class Blog_comments(models.Model):
    blogpost = models.ForeignKey(
        Blog, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    content = models.TextField()

    def __str__(self):
        return f'{str(self.author)}, {self.blogpost.title[:30]}'


class Notification(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_receiver')
    is_read = models.BooleanField()
    category = models.CharField(max_length=10)
    notification_date = models.DateTimeField(default=timezone.now)
    post_id = models.IntegerField(default=-1)

    def __str__(self):
        return f'From:{str(self.sender)} | To: {str(self.receiver)} | Category: {str(self.category)}'


