from django.urls import include, path
from rest_framework import routers, urlpatterns
from .views import BlogGenericDetailAPIView, UserViewSet, BlogViewSet, ViewPostViewSet, blog_list, blog_detail, BlogAPIView, BlogDetailAPIView, BlogGenericAPIView, BlogGenericAPIView

router = routers.DefaultRouter()


'''
1. To get user data - /api/users/?username=<username>
2. To get all posts of a user - /api/posts/?username=<username>
3. To view a post = /api/view_post/?post_id=<id>
'''
urlpatterns = [
    path('users/', UserViewSet.as_view({'get': 'list'})),
    path('posts/', BlogViewSet.as_view()),
    path('view_post/', ViewPostViewSet.as_view()),
    #path('blogs/', blog_list),
    path('blogs/', BlogAPIView.as_view()),
    #path('blog/<int:pk>/', blog_detail),
    path('blog/<int:pk>/', BlogDetailAPIView.as_view()),
    path('generic/blog/<int:pk>/', BlogGenericDetailAPIView.as_view()),
    path('generic/blogs/', BlogGenericAPIView.as_view()),
]
