import json
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
        self.user2 = User.objects.create_user(
            username='Test1', first_name='Testname1', last_name='Last1', email='test1@gmail.com', password='testing@123')
        self.post1 = Blog.objects.create(
            title='Post1', description='Some content', author=self.user1)
        self.post2 = Blog.objects.create(
            title='Post2', description='Some extra content', author=self.user2)
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
        response = self.client.post(reverse('create_post'), {
                                    'title': 'Sample', 'description': 'Some sample description'})
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/create_post/')

    def test_create_blog_if_logged_in_POST(self):
        login = self.client.login(username='Test', password='testing@123')
        self.assertTrue(login)
        response = self.client.post(reverse('create_post'), {
                                    'title': 'Sample', 'description': 'Some sample description'})
        post_id = Blog.objects.last()
        self.assertRedirects(response, reverse(
            'view_post', args=[post_id.id, post_id.slug]))

    def test_vote_up_if_not_logged_in_POST(self):
        response = self.client.post(reverse('vote_up'), data={
                                    'post_id': self.post1.id})
        response_json = json.loads(response.content)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response_json['status'], 'Login Required')

    def test_vote_up_self_post_if_logged_in_POST(self):
        login = self.client.login(username='Test', password='testing@123')
        self.assertTrue(login)
        response = self.client.post(reverse('vote_up'), data={
                                    'post_id': self.post1.id})
        response_json = json.loads(response.content)
        # print(response_json)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response_json['status'], 'Invalid')

    def test_vote_up_others_post_if_logged_in_POST(self):
        login = self.client.login(
            username=self.user1.username, password='testing@123')
        self.assertTrue(login)
        response = self.client.post(reverse('vote_up'), data={
                                    'post_id': self.post2.id})
        response_json = json.loads(response.content)
        # print(response_json)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response_json['status'], 'success')

    def test_vote_down_if_not_logged_in_POST(self):
        response = self.client.post(reverse('vote_down'), data={
                                    'post_id': self.post1.id})
        response_json = json.loads(response.content)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response_json['status'], 'Login Required')

    def test_vote_down_self_post_if_logged_in_POST(self):
        login = self.client.login(username='Test', password='testing@123')
        self.assertTrue(login)
        response = self.client.post(reverse('vote_down'), data={
                                    'post_id': self.post1.id})
        response_json = json.loads(response.content)
        # print(response_json)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response_json['status'], 'Invalid')

    def test_vote_down_others_post_if_logged_in_POST(self):
        login = self.client.login(
            username=self.user1.username, password='testing@123')
        self.assertTrue(login)
        response = self.client.post(reverse('vote_down'), data={
                                    'post_id': self.post2.id})
        response_json = json.loads(response.content)
        # print(response_json)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response_json['status'], 'success')

    
    # Vote up and vote down simultaneously
    # vote down and vote up simultaneously
    # Vote up and vote up on same post
    # Vote down and vote down on same post
