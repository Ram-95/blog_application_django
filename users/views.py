from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from blogs.models import Blog
from .forms import UserRegisterForm
from django.contrib.auth.models import User


def register(request):
    form = UserRegisterForm()
    title = 'Register'
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # This statement will save the form contents to the Users table in the DB
            form.save()
            #username = form.cleaned_data.get('username')
            messages.success(
                request, f'Your account has been created successfully. You can now login')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form, 'title': title})


@login_required
def profile(request):
    '''Shows current logged in users profile'''
    user = request.user
    user_blogs = user.blog_set.all()
    title = 'My Profile'
    context = {
        'user_blogs': user_blogs,
        'title': title,
    }
    # print(user.blog_set.all())
    return render(request, 'users/profile.html', context)

@login_required
def view_profile(request, username):
    '''Allows users to view other users profile'''
    user = get_object_or_404(User, username=username)
    #user = User.objects.filter(username=username).first()
    user_blogs = user.blog_set.all()
    title = username
    context = {
        'user': user,
        'user_blogs': user_blogs,
        'title': title,
    }
    # print(user.blog_set.all())
    return render(request, 'users/view_profile.html', context)
