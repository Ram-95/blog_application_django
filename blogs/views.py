from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.http import HttpResponse
from .models import Blog
from django.contrib.auth.models import User
from django.db.models import Count
# Class based View
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
        #context = super().get_context_data(**kwargs)
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
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ['title', 'description']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# Class based view to Update a post
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Blog
    fields = ['title', 'description']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    # Checks if the post that is to be updated belongs to the current logged user
    def test_func(self):
        post = self.get_object()
        # Checks if the author of post is same as the logged in user
        if self.request.user == post.author:
            return True
        return False

# Class based view to Update a post
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = Blog
    success_url = '/'
    # Checks if the post that is to be deleted belongs to the current logged user
    def test_func(self):
        post = self.get_object()
        # Checks if the author of post is same as the logged in user
        if self.request.user == post.author:
            return True
        return False



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
