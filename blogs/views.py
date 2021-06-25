from users.views import profile
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import json
from django.utils import timezone
from .forms import CommentForm
# To use messages in Class based views - Use SuccessMessageMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, JsonResponse
from .models import Blog, Likes_Table, Blog_comments, Notification
from django.contrib.auth.models import User
from users.models import Profile
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
    # Will display 4 posts on a page.
    paginate_by = 4
    ordering = ['-publish_date']

    def get_context_data(self, **kwargs):
        # This function is used to add extra details to context.
        # Fetching the context details of the PostListView class
        # will have the queryset - object_list and pagination details like - paginator, page_obj, is_paginated
        blogs_list = super().get_context_data(**kwargs)
        # print(blogs_list)
        # Adding the extra data that we'd like to store in context
        # context['now'] = timezone.now()
        # Gets the top 5 visited/Liked posts
        # NOTE:
        # blogs_list_top5 = blogs_list['object_list'].order_by('-likes')[:5] will also work provided paginate_by
        # is NOT set
        blogs_list_top5 = Blog.objects.order_by('-likes')[:5]
        blogs_list_top_viewed = Blog.objects.order_by('-views')[:5]

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
            'blogs_list_top_viewed': blogs_list_top_viewed,
        }
        # If some user is logged in, then get the posts that are upvoted/downvoted by the logged in user
        # and show the colors appropriately.
        if self.request.user.is_authenticated:
            user = self.request.user
            notification_exists = Notification.objects.filter(
                receiver=user, is_read=False).count()
            vote_qs = Likes_Table.objects.filter(user_id=user.id)
            votes = {}
            # Add the {post_id: like_status_id} of every vote by the current logged in user.
            for i in vote_qs:
                votes[i.post_id.id] = i.like_status_id
            # Adding the votes dictionary to the context
            context['votes'] = votes
            context['notification_exists'] = notification_exists

        # Merging the 'context' dictionary and 'blogs_list' dictionary and sending the context as response
        # to be used in the template
        context = {**context, **blogs_list}
        return context


class PostDetailView(DetailView):
    '''Post Detail View'''
    model = Blog
    template_name = 'blogs/view_post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog = self.get_object()
        pk = blog.pk
        # Logic to increment views - If the author of post, views the post then the views are not incremented.
        if self.request.user.is_authenticated:
            if blog.author != self.request.user:
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
        # Inserting the Notification details into the Table
        post = self.get_object()
        post_author = post.author
        # Do NOT send any notification if a user has commented on his own post
        if post_author != self.request.user:
            n = Notification(sender=self.request.user, receiver=post_author,
                             is_read=False, category='comment', post_id=post.pk)
            n.save()
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
                # If post is already downvoted, then increment the counter and mark like_status as True
                lt_post = Likes_Table.objects.filter(
                    user_id=request.user, post_id=post.pk).first()
                lt_post.like_status_id = True
                lt_post.save()
                post.likes += 1
                post.save()
                return JsonResponse({'status': 'success'})
            elif posts_liked.get(post.pk, None) is True:
                # if the post is already upvoted by the user, No Action
                print('User has Already Upvoted the post')
                return JsonResponse({'status': 'Already Upvoted.'})
            else:
                # If the post is not present in the table, increment the counter and insert record as True
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
            posts_unliked = {}
            u = request.user.likes_table_set.all()
            for i in u:
                posts_unliked[i.post_id.pk] = i.like_status_id
            print(f'Vote Down: {posts_unliked}')

            if posts_unliked.get(post.pk, None) is True:
                # If post is already upvoted, then decrement the counter and mark like_status as False
                lt_post = Likes_Table.objects.filter(
                    user_id=request.user, post_id=post.pk).first()
                lt_post.like_status_id = False
                lt_post.save()
                post.likes -= 1
                post.save()
                return JsonResponse({'status': 'success'})
            elif posts_unliked.get(post.pk, None) is False:
                # If post is already downvoted, then No Action
                print('Already Downvoted')
                return JsonResponse({'status': 'Already Downvoted'})
            else:
                # If post is not present in table, then decrement counter and insert record as False
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
def refresh_comments(request):
    if request.user.is_authenticated and request.method == 'GET':
        blog_id = request.GET.get('post_id')
        no_of_comments = Blog_comments.objects.filter(blogpost=blog_id).count()
        return JsonResponse({'no_of_comments': no_of_comments})
    else:
        return HttpResponse('Request method is not GET')


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


@csrf_exempt
@login_required
def notifications(request):
    if request.user.is_authenticated:
        unread_notifs = Notification.objects.get_notification_count(request.user)
        read_notifs = Notification.objects.filter(
            receiver=request.user, is_read=True).order_by('-notification_date')
        profile_pics = {}
        for i in read_notifs:
            temp = Profile.objects.filter(user=i.sender).first().profile_pic.url
            if i.sender not in profile_pics:
                profile_pics[i.sender] = temp
    
        context = {
            'unread_notifications': unread_notifs,
            'notifications_count': len(unread_notifs),
            'read_notifications': read_notifs,
            'profile_imgs': profile_pics,
        }

    return render(request, 'blogs/notifications.html', context)


@csrf_exempt
@login_required
def mark_notification_as_read(request):
    if request.user.is_authenticated:
        notif_id = request.POST['n_post_id']
        if notif_id == -1:
            n = Notification.objects.filter(
                receiver=request.user, is_read=False).update(is_read=True)
        else:
            n = Notification.objects.filter(
                post_id=notif_id, is_read=False).update(is_read=True)

        return JsonResponse({'status': 'success'})


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
