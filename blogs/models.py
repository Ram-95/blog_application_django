from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Count
from users.models import Profile


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
        notifs_count = (Notification.objects.filter(is_read=False, receiver=user).values(
            'receiver', 'category', 'post_id').annotate(dcount=Count('id')))
        
        # List to store the required data as dictionary.
        notif_data = list()

        for item in notifs_count:
            n_post_id = item['post_id']
            n_count = item['dcount'] - 1
            
            # If Notification is of type 'follow'
            if n_post_id == -1:
                n_sender = Notification.objects.filter(
                    receiver=user, category='follow', is_read=False).first().sender
                n_timestamp = Notification.objects.filter(
                    receiver=user, category='follow', is_read=False).first().notification_date
            else:
                n_sender = Notification.objects.filter(
                    post_id=n_post_id, receiver=user, is_read=False).first().sender
                n_timestamp = Notification.objects.filter(
                    post_id=n_post_id, is_read=False).first().notification_date
            n_profile_pic = Profile.objects.filter(user=n_sender).first().profile_pic.url

            # Appending the above data as dictionary to notif_data list
            notif_data.append({'n_post_id': n_post_id, 'n_count': n_count, 'n_sender': n_sender.username,
                               'n_timestamp': n_timestamp, 'n_profile_pic': n_profile_pic})
        
        # Sorting the list of dictionaries based on the timestamp in ascending order
        notif_data.sort(key=lambda x: x['n_timestamp'], reverse=True)
        
        return notif_data
        


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
