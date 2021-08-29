from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import Profile


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2']

    def clean(self):
        """Form Validations"""
        cd = self.cleaned_data
        cd_username = cd.get('username')
        if User.objects.filter(username=cd_username).exists():
            raise ValidationError('Username already taken.')
        cd_email = cd.get('email')
        if User.objects.filter(email=cd_email).exists():
            raise ValidationError('Account with this email already exists.')

        return cd


# Updates the User Model
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


# Updates the Profile Model
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic']
