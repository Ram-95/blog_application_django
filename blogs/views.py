from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import json
# To use messages in Class based views - Use SuccessMessageMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, JsonResponse
from .models import Blog, Likes_Table
from django.contrib.auth.models import User
from django.db.models import Count
from django.contrib import messages
# Class based View - List, Detail, Create,Update, Delete
from django.views.generic import (ListView, CreateView, UpdateView, DeleteView)
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


''' Function Based View'''
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


''' Class Based View - ListView'''
class PostListView(ListView):
    model = Blog
    template_name = 'blogs/index.html'

    def get_context_data(self, **kwargs):
        '''This function is used to add extra details to context.'''
        # Fetching the context details of the Super class
        #context = super().get_context_data(**kwargs)
        # Adding the extra data that we'd like to store in context
        #context['now'] = timezone.now()
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

        return context


# Class Based View to create a post - The file it takes is <app>/<model>_form.html
class PostCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Blog
    fields = ['title', 'description', 'image']
    success_message = 'Post created successfully.'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        '''Function to pass the context data to the HTML page. Here I am adding title of the page to context.'''
        context = super().get_context_data(**kwargs)
        context['title'] = 'New Post'
        return context
    

# Class based view to Update a post
class PostUpdateView(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Blog
    fields = ['title', 'description', 'image']
    success_message = 'Post Updated successfully.'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        '''Function to pass the context data to the HTML page. Here I am adding title of the page to context'''
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Post'
        return context

    # Checks if the post that is to be updated belongs to the current logged user
    def test_func(self):
        post = self.get_object()
        # Checks if the author of post is same as the logged in user
        if self.request.user == post.author:
            return True
        return False


# Class based view to Delete a post
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Blog
    success_url = '/'
    # Checks if the post that is to be deleted belongs to the current logged user

    def test_func(self):
        post = self.get_object()
        # Checks if the author of post is same as the logged in user
        if self.request.user == post.author:
            return True
        return False

    def get_context_data(self, **kwargs):
        '''Function to pass the context data to the HTML page. Here I am adding title of the page to context'''
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Post'
        return context


def view_post(request,pk):
    # Shows a particular post based on it's PK passed via URL
    blog = get_object_or_404(Blog, pk=pk)
    # Dictionary to store the posts liked by the current logged in user.
    # Stores {<post_id>: <like_status>}
    posts_liked = {}
    if request.user.is_authenticated:
        u = request.user.likes_table_set.all()
        for i in u:
            posts_liked[i.post_id.pk] = i.like_status_id
        print(posts_liked) 
    title = blog.title
    context = {
        'blog': blog,
        'title': title,
        'posts_liked': posts_liked,
    }
    return render(request, 'blogs/view_post.html', context)


@csrf_exempt
#@login_required
def vote_up(request):
    if request.user.is_authenticated and request.method == 'POST':
        post_id = request.POST['post_id']
        post = Blog.objects.get(id=post_id)
        print(f'Post PK: {post.pk}')
        if request.user != post.author:
            # Dictionary to store the posts liked by the current logged in user. Stores {<post_id>: <like_status>}
            posts_liked = {}
            u = request.user.likes_table_set.all()
            for i in u:
                posts_liked[i.post_id.pk] = i.like_status_id
            print(f'Vote UP: {posts_liked}')
            
            if posts_liked.get(post.pk, None) is False:
            # If post is already downvoted, then increment the counter and delete the record
                post.likes += 1
                post.save()
                Likes_Table.objects.filter(user_id=request.user, post_id=post.pk).delete()
                print('Already Downvoted. Removing record.')
                return JsonResponse({'status': 'success'})
            elif posts_liked.get(post.pk, None) is True:
            # if the post is already upvoted by the user, No Action
                print('Already Upvoted')
                return JsonResponse({'status': 'Already Upvoted.'})
            else:
            # If the post is not present in the table, increment the counter and insert as True
                lt_post = Likes_Table(user_id=request.user, post_id=post,like_status_id=True)
                lt_post.save()
                post.likes += 1
                post.save()
                print('Upvote Success. Inserted Record.')
                return JsonResponse({'status': 'success'})
        else:
            print('You cannot like your own post!')
            return JsonResponse({'status': 'You cannot Upvote your own post!'})
    else:
        return JsonResponse({'status': 'Login Required'})


@csrf_exempt
#@login_required
def vote_down(request):
    if request.user.is_authenticated and request.method == 'POST':
        post_id = request.POST['post_id']
        post = Blog.objects.get(id=post_id)
        
        if request.user != post.author:
            # Dictionary to store the posts liked by the current logged in user. Stores {<post_id>: <like_status>}
            posts_liked = {}
            u = request.user.likes_table_set.all()
            for i in u:
                posts_liked[i.post_id.pk] = i.like_status_id
            print(f'Vote Down: {posts_liked}')
            
            if posts_liked.get(post.pk, None) is True:
            # If post is already upvoted, then decrement the counter and delete the record
                post.likes -= 1
                post.save()
                Likes_Table.objects.filter(user_id=request.user, post_id=post.pk).delete()
                print('Already Upvoted. Removing record.')
                return JsonResponse({'status': 'success'})
            elif posts_liked.get(post.pk, None) is False:
            # If post is already downvoted, then No Action
                print('Already Downvoted')
                return JsonResponse({'status': 'Already Downvoted'})
            else:
            # If post is not present in table, then decrement counter and inserted record as False
                post.likes -= 1
                post.save()
                dlt_post = Likes_Table(user_id=request.user, post_id=post, like_status_id=False)
                dlt_post.save()
                print('Downvote Success')
                return JsonResponse({'status': 'success'})
        else:
            print('You cannot downvote your own post!')
            return JsonResponse({'status': 'You cannot Downvote your own post!'})
    else:
        return JsonResponse({'status': 'Login Required'})
    
        
