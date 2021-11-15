from django.db import models
from django.conf import settings

class UsersChatRoom(models.Model):
    title = models.CharField(max_length=200, unique=True, blank=False)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, help_text="users who are in the chat")


    def __str__(self) -> str:
        return self.title

    def connect_user(self, user):
        """Return True if user is connected to the user."""
        is_user_added = False
        