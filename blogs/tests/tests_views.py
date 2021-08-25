from django.test import TestCase, Client
from django.urls import resolve, reverse
from django.contrib.auth.models import User
from blogs.models import Blog, Likes_Table, Blog_comments, Notification

"""
class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.list_url = reverse('index')
        self.user1 = User.objects.create(
            username='Test', first_name='Testname', last_name='Last', email='test@gmail.com', password='testing@123')
        self.post1 = Blog.objects.create(
            title='Post1', description='Some content', author=self.user1)
        self.detail_url = reverse('view_post', args=[self.post1.id, 'post1'])

    def test_blogs_list_GET(self):
        response = self.client.get(self.list_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_blogs_detail_GET(self):
        response = self.client.get(self.detail_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogs/view_post.html')
"""