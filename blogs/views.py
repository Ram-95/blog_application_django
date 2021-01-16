from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import json
from django.utils import timezone
from .forms import CommentForm
# To use messages in Class based views - Use SuccessMessageMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, JsonResponse
from .models import Blog, Likes_Table, Blog_comments
from django.contrib.auth.models import User
from django.db.models import Count
from django.contrib import messages
# Class based View - List, Detail, Create,Update, Delete
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


''' Class Based View - ListView'''
class PostListView(ListView):
    model = Blog
    template_name = 'blogs/index.html'
    #context_object_name = 'blogs_list'
    paginate_by = 3
    ordering = ['-publish_date']


    def get_context_data(self, **kwargs):
        # This function is used to add extra details to context.
        # Fetching the context details of the PostListView class
        # will have the queryset - object_list and pagination details like - paginator, page_obj, is_paginated
        blogs_list = super().get_context_data(**kwargs)
        #print(blogs_list)
        # Adding the extra data that we'd like to store in context
        # context['now'] = timezone.now()
        
        # Gets the top 5 visited/Liked posts
        # NOTE: 
        # blogs_list_top5 = blogs_list['object_list'].order_by('-likes')[:5] will also work provided paginate_by
        # is NOT set
        blogs_list_top5 = Blog.objects.order_by('-likes')[:5]
        

        # Gets the top 5 authors/contributors
        # NOTE: 
        # top_authors = Blog.objects.all().values('author').annotate(
        #    total=Count('author')).order_by('-total')[:5] will also work provided paginate_by is NOT set
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
            'posts': blogs_list['object_list'],
            'title': title,
            'blogs_list_top5': blogs_list_top5,
            'top_authors': authors_list,
        }

        # Merging the 'context' dictionary and 'blogs_list' dictionary and sending the context as response
        # to be used in the template
        context = {**context, **blogs_list}
        # print(f'\n\n{context}')
        return context


class PostDetailView(DetailView):
    '''Post Detail View'''
    model = Blog
    template_name = 'blogs/view_post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog = self.get_object()
        pk = blog.pk
        # Logic to increment views
        view_upd = Blog.objects.filter(pk=pk).first()
        view_upd.views += 1
        view_upd.save()
        
        posts_liked = {}
        title = blog.title
        comments = Blog_comments.objects.filter(
            blogpost=pk).order_by('date_posted')
        no_of_comments = comments.count()
        no_of_likes = Likes_Table.objects.filter(post_id=pk).count()
        context = {
            'blog': blog,
            'title': title,
            'no_of_likes': no_of_likes,
            'comments': comments,
            'no_of_comments': no_of_comments,
        }

        if self.request.user.is_authenticated:
            u = self.request.user.likes_table_set.all()
            comment_form = CommentForm(instance=self.request.user)
            for i in u:
                posts_liked[i.post_id.pk] = i.like_status_id
            # print(posts_liked)
            context['posts_liked'] = posts_liked
            context['comment_form'] = comment_form

        return context

    # This method saves the contents to Blog_comments table
    def post(self, request, *args, **kwargs):
        new_comment = Blog_comments(content=request.POST.get('content'),
                                    author=self.request.user,
                                    blogpost=self.get_object())
        new_comment.save()
        print('Comment Inserted.')
        return self.get(self, request, *args, **kwargs)



# Class Based View to create a post - The HTML file it takes is <app>/<model>_form.html. 
# Can be overriden by "template_name" variable. Eg. template_name = 'file.html' 
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


# Function based view - Not currently using
def view_post(request, pk):
    # Shows a particular post based on it's PK passed via URL
    blog = get_object_or_404(Blog, pk=pk)
    # Dictionary to store the posts liked by the current logged in user.
    # Stores {<post_id>: <like_status>}
    posts_liked = {}
    title = blog.title
    comments = Blog_comments.objects.filter(
        blogpost=pk).order_by('-date_posted')
    no_of_comments = comments.count()
    no_of_likes = Likes_Table.objects.filter(post_id=pk).count()
    context = {
        'blog': blog,
        'title': title,
        'no_of_likes': no_of_likes,
        'comments': comments,
        'no_of_comments': no_of_comments,
    }

    if request.user.is_authenticated:
        u = request.user.likes_table_set.all()
        comment_form = CommentForm(instance=request.user)
        for i in u:
            posts_liked[i.post_id.pk] = i.like_status_id
        # print(posts_liked)
        context['posts_liked'] = posts_liked
        context['comment_form'] = comment_form

    return render(request, 'blogs/view_post.html', context)


@csrf_exempt
# @login_required
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
                Likes_Table.objects.filter(
                    user_id=request.user, post_id=post.pk).delete()
                print('Already Downvoted. Removing record.')
                return JsonResponse({'status': 'success'})
            elif posts_liked.get(post.pk, None) is True:
                # if the post is already upvoted by the user, No Action
                print('Already Upvoted')
                return JsonResponse({'status': 'Already Upvoted.'})
            else:
                # If the post is not present in the table, increment the counter and insert as True
                lt_post = Likes_Table(
                    user_id=request.user, post_id=post, like_status_id=True)
                lt_post.save()
                post.likes += 1
                post.save()
                print('Upvote Success. Inserted Record.')
                return JsonResponse({'status': 'success'})
        else:
            print('You cannot like your own post!')
            return JsonResponse({'status': 'Invalid'})
    else:
        return JsonResponse({'status': 'Login Required'})


@csrf_exempt
# @login_required
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
                Likes_Table.objects.filter(
                    user_id=request.user, post_id=post.pk).delete()
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
                dlt_post = Likes_Table(
                    user_id=request.user, post_id=post, like_status_id=False)
                dlt_post.save()
                print('Downvote Success')
                return JsonResponse({'status': 'success'})
        else:
            print('You cannot downvote your own post!')
            return JsonResponse({'status': 'Invalid'})
    else:
        return JsonResponse({'status': 'Login Required'})


@csrf_exempt
def delete_comment(request):
    if request.user.is_authenticated and request.method == 'POST':
        comment_id = request.POST['comment_id']
        Blog_comments.objects.filter(pk=comment_id).delete()
        #print(f'Comment Deleted!')
        return HttpResponse('success')
    else:
        return HttpResponse('Request method is not POST')


@csrf_exempt
def edit_comment(request):
    if request.user.is_authenticated and request.method == 'POST':
        comment_id = request.POST['comment_id']
        edit_comment = request.POST['edit_comment']
        bc = Blog_comments.objects.filter(pk=comment_id).first()
        bc.content = edit_comment
        bc.date_posted = timezone.now()
        bc.save()
        #print('Comment Edit Saved!')
        return HttpResponse('success')
    else:
        return HttpResponse('Request method is not POST')


''' Function Based View - Index'''
'''
def index(request):
    # Views the Homepage.
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
'''