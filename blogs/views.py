from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Blog
from django.contrib.auth.models import User
from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


def index(request):
    ''' Views the Homepage. '''
    # Gets all the blogs by all the users
    blogs_list = Blog.objects.order_by('-publish_date')

    # Gets the top 5 visited/Liked posts - INCOMPLETE
    blogs_list_top5 = Blog.objects.order_by('-likes')[:5]

    # Gets the top 5 authors/contributors
    top_authors = Blog.objects.all().values('author').annotate(
        total=Count('author')).order_by('-total')[:5]
    # List to store the top 5 authors usernames
    authors_list = []
    # Iterating over the top 5 authors queryset and extracting their usernames
    for i in top_authors:
        authors_list.append(User.objects.filter(
            id=i['author']).first().username)

    title = 'Home'
    context = {
        'blogs_list': blogs_list,
        'title': title,
        'blogs_list_top5': blogs_list_top5,
        'top_authors': authors_list,
    }
    return render(request, 'blogs/index.html', context)


def create_post(request):
    # Passes the title of the webpage to the base.html file
    title = 'Create New Post'
    return render(request, 'blogs/create_post.html', {'title': title})


def view_post(request, pk):
    # Shows a particular post based on it's ID passed via URL
    blog = get_object_or_404(Blog, pk=pk)
    title = 'Post ' + str(pk)
    context = {
        'blog': blog,
        'title': title,
    }
    return render(request, 'blogs/view_post.html', context)


@csrf_exempt
@login_required
def vote_up(request):
    if request.method == 'POST':
        post_id = request.POST['post_id']
        post = Blog.objects.get(id=post_id)
        post.likes += 1
        post.save()
        return HttpResponse('Upvote Done')
    else:
        return HttpResponse('Request Method is not Post.')


@csrf_exempt
def vote_down(request):
    if request.method == 'POST':
        post_id = request.POST['post_id']
        post = Blog.objects.get(id=post_id)
        post.likes -= 1
        post.save()
        return HttpResponse('Downvote Done')
    else:
        return HttpResponse('Request Method is not Post.')
