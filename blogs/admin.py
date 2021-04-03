from django.contrib import admin
from . models import Blog, Likes_Table, Blog_comments, Notification

# Register your models here.
admin.site.register(Blog)
admin.site.register(Likes_Table)
admin.site.register(Blog_comments)
admin.site.register(Notification)
