from django.urls import include, path
from rest_framework import routers, urlpatterns
from .views import UserViewSet, BlogViewSet, ViewPostViewSet

router = routers.DefaultRouter()


'''
1. To get user data - /api/users/?username=<username>
2. To get all posts of a user - /api/posts/?username=<username>
3. To view a post = /api/view_post/?post_id=<id>
'''
urlpatterns = [
    path('api/users/', UserViewSet.as_view({'get': 'list'})),
    path('api/posts/', BlogViewSet.as_view()),
    path('api/view_post/', ViewPostViewSet.as_view()),
]
