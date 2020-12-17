from django.shortcuts import render
from django.http import HttpResponse
from .models import Blog


def index(request):
    blogs_list = Blog.objects.order_by('-publish_date')
    context = {
        'blogs_list': blogs_list
    }
    return render(request, 'blogs/index.html', context)


def create_post(request):
    # Passes the title of the webpage to the base.html file
    title = 'Create New Post'
    return render(request, 'blogs/create_post.html', {'title': title})
