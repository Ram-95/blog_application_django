from django.test import SimpleTestCase, Client
from django.urls import resolve, reverse
from blogs.views import *


class TestURLs(SimpleTestCase):
    """Tests to check if the URLs are properly resolved."""

    def test_index_is_resolved(self):
        url = reverse('index')
        self.assertEquals(resolve(url).func.view_class, PostListView)

    def test_view_post_is_resolved(self):
        url = reverse('view_post', args=[1])
        self.assertEquals(resolve(url).func.view_class, PostDetailView)
    
    def test_view_post_with_slug_is_resolved(self):
        url = reverse('view_post', args=[1, 'some-slug'])
        self.assertEquals(resolve(url).func.view_class, PostDetailView)

    def test_create_post_is_resolved(self):
        url = reverse('create_post')
        self.assertEquals(resolve(url).func.view_class, PostCreateView)

    def test_update_post_is_resolved(self):
        url = reverse('update_post', args=[1])
        self.assertEquals(resolve(url).func.view_class, PostUpdateView)

    def test_delete_post_is_resolved(self):
        url = reverse('delete_post', args=[1])
        self.assertEquals(resolve(url).func.view_class, PostDeleteView)

    def test_delete_comment_is_resolved(self):
        url = reverse('delete_comment')
        self.assertEquals(resolve(url).func, delete_comment)

    def test_edit_comment_is_resolved(self):
        url = reverse('edit_comment')
        self.assertEquals(resolve(url).func, edit_comment)

    def test_refresh_comments_is_resolved(self):
        url = reverse('refresh_comments')
        self.assertEquals(resolve(url).func, refresh_comments)

    def test_vote_up_is_resolved(self):
        url = reverse('vote_up')
        self.assertEquals(resolve(url).func, vote_up)

    def test_vote_down_is_resolved(self):
        url = reverse('vote_down')
        self.assertEquals(resolve(url).func, vote_down)

    def test_notifications_is_resolved(self):
        url = reverse('notifications')
        self.assertEquals(resolve(url).func, notifications)

    def test_mark_notification_as_read_is_resolved(self):
        url = reverse('mark_notification_as_read')
        self.assertEquals(resolve(url).func, mark_notification_as_read)

    def test_search_is_resolved(self):
        url = reverse('search')
        self.assertEquals(resolve(url).func, search)

    def test_search_user_is_resolved(self):
        url = reverse('searchUser')
        self.assertEquals(resolve(url).func, searchModel)
