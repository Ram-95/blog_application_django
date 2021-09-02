import json
from django.test import TestCase, Client
from django.contrib.auth.models import User
from users.models import Profile, Followers
from django.urls import reverse
from django.contrib.auth import views as auth_views


class TestUserViews(TestCase):
    """Tests the views of Users application."""

    def setUp(self):
        self.user1 = User.objects.create_user(
            username='Test', first_name='Testname', last_name='Last', email='test@gmail.com', password='testing@123')
        self.user2 = User.objects.create_user(
            username='Test1', first_name='Testname1', last_name='Last1', email='test1@gmail.com', password='testing@123')
        self.profile1 = Profile.objects.get(user=self.user1)
        self.profile2 = Profile.objects.get(user=self.user2)

    def test_user_register(self):
        data = {
            'username': 'gibbsh',
            'first_name': 'Gibberish',
            'last_name': 'name',
            'email': 'test_mail1@email.com',
            'password1': 'Testing@123',
            'password2': 'Testing@123',
        }
        response = self.client.post(reverse('register'), data=data)
        user_created = User.objects.filter(username=data['username']).exists()
        self.assertTrue(user_created)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_user_logged_in(self):
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, 'users/login.html')

    def test_user_logged_out(self):
        response = self.client.get(reverse('logout'))
        self.assertTemplateUsed(response, 'users/logout.html')

    def test_password_reset_view(self):
        response = self.client.get(reverse('password_reset'))
        self.assertTemplateUsed(response, 'users/password_reset.html')

    def test_password_reset_done_view(self):
        response = self.client.get(reverse('password_reset_done'))
        self.assertTemplateUsed(response, 'users/password_reset_done.html')

    def test_password_reset_complete(self):
        response = self.client.get(reverse('password_reset_complete'))
        self.assertTemplateUsed(response, 'users/password_reset_complete.html')

    def test_profile_GET_if_not_logged_in(self):
        response = self.client.get(
            reverse('profile', args=[self.user1.username]))
        self.assertRedirects(response, '/login/?next=/profile/Test/')

    def test_profile_GET_if_logged_in_self_profile(self):
        # To login the user
        login = self.client.login(
            username=self.user1.username, password='testing@123')
        response = self.client.get(
            reverse('profile', args=[self.user1.username]))
        # Check if the user is successfully logged in
        self.assertEquals(str(response.context['user']), self.user1.username)
        # Check that the status_code is 200 i.e. Success
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/view_profile.html')

    def test_profile_GET_if_logged_in_other_profile(self):
        login = self.client.login(
            username=self.user1.username, password='testing@123')
        response = self.client.get(
            reverse('profile', args=[self.user2.username]))
        self.assertEquals(str(response.context['user']), self.user1.username)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/view_profile.html')

    def test_view_followers_GET_if_not_logged_in(self):
        response = self.client.get(
            reverse('view_followers', args=[self.user1.username]))
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/view_followers/Test/')

    def test_view_followers_GET_if_logged_in(self):
        login = self.client.login(
            username=self.user1.username, password='testing@123')
        response = self.client.get(
            reverse('view_followers', args=[self.user1.username]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/followers.html')

    def test_follow_a_user_if_not_logged_in(self):
        response = self.client.get(reverse('follow'))
        self.assertRedirects(response, '/login/?next=/follow/')
        self.assertEquals(response.status_code, 302)

    def test_follow_a_user_if_logged_in(self):
        login = self.client.login(
            username=self.user1.username, password='testing@123')
        self.assertTrue(login)
        response = self.client.post(reverse('follow'), data={
                                    'username': self.user2.username})
        json_status = json.loads(response.content)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json_status['status'], 'success')
        # Checking if entry added to DB
        f = Followers.objects.get(id=1)
        self.assertEquals(f.user, self.profile1)
        self.assertEquals(f.followers, self.profile2)

    def test_unfollow_a_user_if_not_logged_in(self):
        response = self.client.get(reverse('unfollow'))
        self.assertRedirects(response, '/login/?next=/unfollow/')
        self.assertEquals(response.status_code, 302)

    def test_unfollow_a_user_if_logged_in(self):
        login = self.client.login(username='Test', password='testing@123')
        self.assertTrue(login)
        response = self.client.get(reverse('unfollow'))
        self.assertEquals(response.status_code, 200)

    # Read this thoroughly: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing
