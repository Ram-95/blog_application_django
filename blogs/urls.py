from django.urls import path
from .views import PostListView, PostCreateView, PostUpdateView, PostDeleteView
from . import views


urlpatterns = [
    path('', PostListView.as_view(), name="index"),
    path('create_post/', PostCreateView.as_view(), name="create_post"),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name="update_post"),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name="delete_post"),
    path('post/<int:pk>/', views.view_post, name="view_post"),
    path('vote_up/', views.vote_up, name="vote_up"),
    path('vote_down/', views.vote_down, name="vote_down"),
]
