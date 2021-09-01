from django.test import TestCase, Client
from django.urls import resolve, reverse
from django.contrib.auth.models import User
from blogs.models import Blog, Likes_Table, Blog_comments, Notification


class TestViews(TestCase):
    """Tests to check the functionality of Views in Blogs application"""

    def setUp(self):
        self.client = Client()
        self.list_url = reverse('index')
        self.user1 = User.objects.create_user(
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

    def test_create_blog_if_not_logged_in_POST(self):
        response = self.client.post(reverse('create_post'), {'title': 'Sample', 'description': 'Some sample description'})
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/create_post/')
    
    
    def test_create_blog_if_logged_in_POST(self):
        login = self.client.login(username='Test', password='testing@123')
        self.assertTrue(login)
        response = self.client.post(reverse('create_post'), {'title': 'Sample', 'description': 'Some sample description'})
        post_id = Blog.objects.last()
        self.assertRedirects(response, reverse('view_post', args=[post_id.id, post_id.slug]))
    

        
        
