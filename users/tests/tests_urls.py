from django.test import SimpleTestCase
from django.urls import resolve, reverse
from users.views import *
from django.contrib.auth import views as auth_views


class TestURLs(SimpleTestCase):
    """Test to check if URLs resovle correctly."""

    def test_register_is_resolved(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func, register)

    def test_login_is_resolved(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func.view_class, auth_views.LoginView)

    def test_logout_is_resolved(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func.view_class, auth_views.LogoutView)

    def test_password_reset_is_resolved(self):
        url = reverse('password_reset')
        self.assertEquals(resolve(url).func.view_class,
                          auth_views.PasswordResetView)

    def test_password_reset_done_is_resolved(self):
        url = reverse('password_reset_done')
        self.assertEquals(resolve(url).func.view_class,
                          auth_views.PasswordResetDoneView)

    def test_password_reset_complete_is_resolved(self):
        url = reverse('password_reset_complete')
        self.assertEquals(resolve(url).func.view_class,
                          auth_views.PasswordResetCompleteView)

    def test_profile_is_resolved(self):
        url = reverse('profile', args=['SomeUser'])
        self.assertEquals(resolve(url).func, profile)

    def test_update_profile_is_resolved(self):
        url = reverse('update_profile')
        self.assertEquals(resolve(url).func, update_profile)

    def test_follow_is_resolved(self):
        url = reverse('follow')
        self.assertEquals(resolve(url).func, follow)

    def test_unfollow_is_resolved(self):
        url = reverse('unfollow')
        self.assertEquals(resolve(url).func, unfollow)

    def test_view_followers_is_resolved(self):
        url = reverse('view_followers', args=['SomeUser'])
        self.assertEquals(resolve(url).func, view_followers)
