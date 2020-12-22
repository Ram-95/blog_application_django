from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from blogs.models import Blog


def register(request):
    form = UserCreationForm()
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
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form, 'title': title})


@login_required
def profile(request):
    user = request.user
    user_blogs = user.blog_set.all()
    context = {
        'user_blogs': user_blogs,
    }
    #print(user.blog_set.all())
    return render(request, 'users/profile.html', context)
