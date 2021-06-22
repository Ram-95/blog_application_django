from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Count


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


# Custom managers to get the Number of comments/follows data from Notification Table.
# Refer: https://docs.djangoproject.com/en/dev/topics/db/managers/#custom-managers
# This is used to show notifications like example
# Comment: Rambabu and 2 others commented on your post
# Follow: John and 3 others started following you
class NotificationManager(models.Manager):
    def get_notification_count(self, user):
        # Gets the comments data grouped by (post_id, receiver, category) which are not read
        comments_count = (Notification.objects.filter(is_read=False, category='comment', receiver=user).values(
            'receiver', 'category', 'post_id').annotate(dcount=Count('id')))
        
        # Gets the follow data grouped by (receiver, category) which are not read
        follow_count = (Notification.objects.filter(is_read=False, category='follow', receiver=user).values(
            'receiver', 'category').annotate(dcount=Count('id')))

        # List that stores the comments data - 'c_post_id', 'sender', 'count' as dictionary
        comment_data = []
        # List that stores the follow data - 'f_sender', 'f_count' as dictionary
        follow_data = []
        # Iterating over each comment item and getting a random sender who made that comment
        if comments_count:
            for item in comments_count:
                c_post_id = item['post_id']
                # Selecting the first sender who made this comment
                c_sender = Notification.objects.filter(
                    post_id=c_post_id, receiver=user).first().sender.username
                c_count = item['dcount'] - 1
                comment_data.append(
                    {'c_post_id': c_post_id, 'sender': c_sender, 'count': c_count})

        # Iterating over each follow item and getting a random sender follows the user
        if follow_count:
            for item in follow_count:
                # Selecting the first sender who follows this user
                f_sender = Notification.objects.filter(
                    receiver=user, category='follow', is_read=False).first().sender.username
                f_count = item['dcount'] - 1
                follow_data.append({'f_sender': f_sender, 'f_count': f_count})

        return (comment_data, follow_data)


class Notification(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='notification_sender')
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='notification_receiver')
    is_read = models.BooleanField()
    category = models.CharField(max_length=10)
    notification_date = models.DateTimeField(default=timezone.now)
    post_id = models.IntegerField(default=-1)
    objects = NotificationManager()

    def __str__(self):
        return f'From: {str(self.sender)} | To: {str(self.receiver)} | Category: {str(self.category)}'
