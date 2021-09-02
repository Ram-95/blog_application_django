from django.test import TestCase
from users.models import Profile, Followers
from django.contrib.auth.models import User


class TestModels(TestCase):
    """Tests to check the models of Users application."""

    def setUp(self):
        self.user1 = User.objects.create(
            username='Test', first_name='Testname', last_name='Last', email='test@gmail.com', password='testing@123')
        self.user2 = User.objects.create(
            username='Test2', first_name='Testname2', last_name='Last2', email='test2@gmail.com', password='testing2@123')

    def test_user_label(self):
        profile = Profile.objects.get(user=self.user1)
        field_label = profile._meta.get_field('user').verbose_name
        self.assertEquals(field_label, 'user')

    def test_profile_pic_label(self):
        profile = Profile.objects.get(user=self.user1)
        field_label = profile._meta.get_field('profile_pic').verbose_name
        self.assertEquals(field_label, 'profile pic')

    def test_object_name_is_correct(self):
        profile = Profile.objects.get(user=self.user1)
        actual_value = f"{profile.user.username}'s Profile"
        self.assertEquals(actual_value, str(profile))

    def test_if_user_is_created(self):
        u = User.objects.filter(id=self.user1.id).exists()
        self.assertTrue(u)

    def test_if_user_is_deleted(self):
        User.objects.get(username=self.user2).delete()
        u = User.objects.filter(id=self.user2.id).exists()
        self.assertFalse(u)

    def test_if_correct_details_of_user_captured(self):
        self.assertEquals(self.user1.username, 'Test')
        self.assertEquals(self.user1.first_name, 'Testname')
        self.assertEquals(self.user1.last_name, 'Last')
        self.assertEquals(self.user1.email, 'test@gmail.com')
        self.assertEquals(self.user1.password, 'testing@123')

    def test_if_profile_is_created_when_user_created(self):
        p = Profile.objects.get(user=self.user1).user
        self.assertEquals(self.user1, p)

    def test_if_profile_is_deleted_when_user_deleted(self):
        User.objects.get(username=self.user2).delete()
        p = Profile.objects.filter(user=self.user2).exists()
        self.assertFalse(p)

    def test_if_default_profile_pic_is_assigned(self):
        p = Profile.objects.get(user=self.user1)
        self.assertEquals(p.profile_pic, 'default.png')

    def test_if_followers_are_created(self):
        profile1 = Profile.objects.get(user=self.user1)
        profile2 = Profile.objects.get(user=self.user2)
        Followers.objects.create(
            user=profile1, followers=profile2)
        follower_exist = Followers.objects.filter(
            user=profile1, followers=profile2).exists()
        self.assertTrue(follower_exist)
