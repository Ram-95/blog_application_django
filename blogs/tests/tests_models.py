from django.test import TestCase
from blogs.models import Blog, Likes_Table, Blog_comments, Notification
from django.contrib.auth.models import User
from users.models import Profile


class TestModels(TestCase):
    """Tests to check Models of Blogs application."""

    def setUp(self):
        self.user1 = User.objects.create(
            username='Test', first_name='Testname', last_name='Last', email='test@gmail.com', password='testing@123')
        self.post1 = Blog.objects.create(
            title='Post1', description='Some content', author=self.user1)
        self.liked = Likes_Table.objects.create(
            user_id=self.user1, post_id=self.post1, like_status_id=True)
        self.comment = Blog_comments.objects.create(
            blogpost=self.post1, author=self.user1, content='First Comment')
        self.profile1 = Profile.objects.get(user=self.user1)

    def test_blog_post_created(self):
        self.assertIsInstance(self.post1, Blog)
        b = Blog.objects.get(id=1)
        self.assertEquals(self.post1.id, b.id)
        self.assertEquals(self.post1.title, b.title)
        self.assertEquals(self.post1.description, b.description)
        self.assertEquals(self.post1.author, b.author)
    
    def test_post_assigned_slug_on_creation(self):
        self.assertEquals(self.post1.slug, 'post1')

    def test_unique_slug_assinged(self):
        post2 = Blog.objects.create(
            title='Post1', description='Some content-2', author=self.user1)
        self.assertNotEquals(self.post1.slug, post2.slug)

    def test_post_liked(self):
        self.assertEquals(self.liked.like_status_id, True)


class TestComments(TestCase):
    """Tests to check the Blog_comments model."""
    def setUp(self):
        self.user1 = User.objects.create(
            username='Test', first_name='Testname', last_name='Last', email='test@gmail.com', password='testing@123')
        self.post1 = Blog.objects.create(
            title='Post1', description='Some content', author=self.user1)
        self.liked = Likes_Table.objects.create(
            user_id=self.user1, post_id=self.post1, like_status_id=True)
        self.comment = Blog_comments.objects.create(
            blogpost=self.post1, author=self.user1, content='First Comment')

    def test_comments_number_of_post(self):
        self.assertEquals(self.post1.number_of_comments(), 1)

    def test_comment_inserted_by_user_for_post(self):
        self.assertEquals(self.comment.blogpost, self.post1)

    def test_comment_inserted_content_post(self):
        self.assertEquals(self.comment.content, 'First Comment')
    
    def test_comment_objects_str_representation(self):
        self.assertEquals(str(self.comment), f'{self.user1.username}, {self.post1.title[:30]}')
    
    def test_comments_of_user_deleted_if_user_is_deleted(self):
        # Deleting a user
        User.objects.get(id=self.user1.id).delete()
        # Check if the all comments of the user are deleted
        comments = Blog_comments.objects.filter(author=self.user1).exists()
        self.assertFalse(comments)

