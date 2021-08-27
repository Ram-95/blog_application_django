from django.test import TestCase,Client
from django.contrib.auth.models import User
from users.models import Profile, Followers
from django.urls import reverse

class TestUserViews(TestCase):
    """Tests the views of Users application."""

    def setUp(self):
        self.user1 = User.objects.create(
            username='Test', first_name='Testname', last_name='Last', email='test@gmail.com', password='testing@123')
        
    def test_profile_GET(self):
        response = self.client.get(reverse('profile', args=[self.user1.username]))
        self.assertEquals(response.status_code, 302)
        self.assertTemplateUsed(response, 'users/view_profile.html')

    # Read this thoroughly: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing