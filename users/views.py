from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def register(request):
    form = UserCreationForm()
    title = 'Register'
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # This statement will save the form contents to the Users table in the DB
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account {username} created successfully.')
            print(f'Account Created!')
            return redirect('create_post')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form, 'title': title})

