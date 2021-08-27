from django.test import TestCase, Client
from django.urls import resolve, reverse
from django.contrib.auth.models import User
from blogs.models import Blog, Likes_Table, Blog_comments, Notification


class TestViews(TestCase):
    """Tests to check the functionality of Views in Blogs application"""

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
        self.assertTemplateUsed(response, 'blogs/index.html')

    def test_blogs_detail_GET(self):
        response = self.client.get(self.detail_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogs/view_post.html')

    def test_create_blog_POST(self):
        response = self.client.post('/create_post', {'title': 'Sample', 'description': 'Some sample description'})
        self.assertEquals(response.status_code, 301)

        
        
