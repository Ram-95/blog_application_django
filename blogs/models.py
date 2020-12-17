from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Blog(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=500)
    publish_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
