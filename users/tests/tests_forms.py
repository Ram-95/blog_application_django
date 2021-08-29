from django.contrib.auth.forms import UserCreationForm
from django.test import TestCase, Client
from users.forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, UserCreationForm


class TestUserForms(TestCase):
    """Tests to check forms of users application."""

    def test_user_created(self):
        data = {
            'username': 'Test',
            'first_name': 'Test',
            'last_name': 'name',
            'email': 'test_mail1@email.com',
            'password1': 'Testing@123',
            'password2': 'Testing@123',
        }
        form = UserRegisterForm(data)
        print(form.errors)
        self.assertTrue(form.is_valid())

    def test_username_already_taken(self):
        data = {
            'username': 'Test',
            'first_name': 'Test',
            'last_name': 'name',
            'email': 'test_mail1@email.com',
            'password1': 'Testing@123',
            'password2': 'Testing@123',
        }
        data1 = {
            'username': 'Test',
            'first_name': 'Test1',
            'last_name': 'name1',
            'email': 'test_mail12@email.com',
            'password1': 'Testing@123',
            'password2': 'Testing@123',
        }

        form = UserRegisterForm(data)
        form1 = UserRegisterForm(data1)
        print(form1.errors)
        self.assertTrue(form.is_valid())
        self.assertTrue(form1.is_valid())