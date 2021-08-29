from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import UpdateView
from .models import Profile, Followers
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from blogs.models import Blog, Notification
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User


def register(request):
    form = UserRegisterForm()
    title = 'Register'

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # This statement will save the form contents to the Users table in the DB
            form.save()
            #username = form.cleaned_data.get('username')
            messages.success(
                request, f'Account is created successfully. You can now login')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form, 'title': title})



@login_required
def profile(request, username):
    '''Allows users to view other users profile'''
    user = get_object_or_404(User, username=username)
    #user = User.objects.filter(username=username).first()
    curr_profile = Profile.objects.filter(user=user).first()
    #profile = Profile.objects.filter(user=request.user).first()
    f = Followers.objects.filter(followers=curr_profile)
    followers = set()
    # print(f'\n{f}\n')
    for i in f:
        followers.add(i.user.user.username)
    print(f'\nUsers Following {user}: {followers}\n')
    user_blogs = user.blog_set.all()
    title = username
    no_of_following = Followers.objects.filter(user=curr_profile).count()
    no_of_followers = Followers.objects.filter(followers=curr_profile).count()
    context = {
        'curr_user': user,
        'user_blogs': user_blogs,
        'title': title,
        'followers': followers,
        'no_of_followers': no_of_followers,
        'no_of_following': no_of_following,
    }
    # print(user.blog_set.all())
    return render(request, 'users/view_profile.html', context)



@login_required
def update_profile(request):
    if request.method == 'POST':
        # The instance argument will fill the form with existing user data
        u_form = UserUpdateForm(request.POST, instance=request.user)
        # request.FILES since we are expecting an Image update
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        curr_username = request.user.username
        # Checking and saving if the forms are valid
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your profile is updated successfully.')
            
            # Redirect to Profile page after successful updation
            return redirect('profile', username=curr_username)
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'users/update_profile.html', context)



@csrf_exempt
@login_required
def view_followers(request, username):
    temp = User.objects.filter(username=username).first()
    user = Profile.objects.filter(user=temp).first()
    #print(f'\nUsername in view_profile: {user} {user.id}\n')
    f = Followers.objects.filter(followers=user)
    g = Followers.objects.filter(user=user)
    #print(f'\nfollowers in view_followers: {user} -> {f}\n')
    #print(f'\nFollowing: {g}\n')
    curr_profile = Profile.objects.filter(
        user=get_object_or_404(User, username=username)).first()
    no_of_following = Followers.objects.filter(user=curr_profile).count()
    no_of_followers = Followers.objects.filter(followers=curr_profile).count()
    context = {
        'followers': f,
        'following': g,
        'curr_user': username,
        'no_of_followers': no_of_followers,
        'no_of_following': no_of_following,
    }
    return render(request, 'users/followers.html', context)


@csrf_exempt
@login_required
def follow(request):
    '''Code to follow a User. Creates a record in Followers table.'''
    if request.method == 'POST':
        profile = Profile.objects.filter(
            user=User.objects.filter(username=request.user).first()).first()
        follower = Profile.objects.filter(user=User.objects.filter(
            username=request.POST['username']).first()).first()
        f = Followers(user=profile, followers=follower)
        f.save()
        # Inserting the record into the Notification table
        receiver = User.objects.filter(username=request.POST['username']).first()
        Notification.objects.add_notification(request.user, receiver, 'follow', -1)
        #n = Notification(sender=request.user, receiver=User.objects.filter(username=request.POST['username']).first(), is_read=False, category='follow')
        #n.save()
        #print(f'\nCreated:\nUser: {req_user.username}\nFollowing: {follower}\n')
        return JsonResponse({'status': 'success'})
    else:
        return HttpResponse('Request method is not POST.')


@csrf_exempt
@login_required
def unfollow(request):
    '''Code to unfollow a User. Deletes a record in Followers table.'''
    if request.method == 'POST':
        profile = Profile.objects.filter(
            user=User.objects.filter(username=request.user).first()).first()
        follower = Profile.objects.filter(user=User.objects.filter(
            username=request.POST['username']).first()).first()
        Followers.objects.filter(user=profile, followers=follower).delete()
        #print(f'\nDeleted:\nUser: {req_user.username}\nFollower: {follower}\n')
        # Deleting the record from Notification table when a exising follower unfollows
        receiver=User.objects.filter(username=request.POST['username']).first()
        Notification.objects.remove_notification(request.user, receiver, 'follow', -1)
        '''
        Notification.objects.filter(sender=request.user, receiver=User.objects.filter(
            username=request.POST['username']).first(), category='follow').delete()
        '''
        return JsonResponse({'status': 'success'})
    else:
        return HttpResponse('Request method is not POST.')
