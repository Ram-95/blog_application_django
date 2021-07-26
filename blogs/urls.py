from django.urls import path
from .views import PostListView, PostCreateView, PostUpdateView, PostDeleteView, PostDetailView
from . import views


urlpatterns = [
    path('', PostListView.as_view(), name="index"),
    path('create_post/', PostCreateView.as_view(), name="create_post"),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name="update_post"),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name="delete_post"),
    path('post/<int:pk>/', PostDetailView.as_view(), name="view_post"),
    path('post/<int:pk>/<slug:slug>/', PostDetailView.as_view(), name="view_post"),
    path('delete_comment/', views.delete_comment, name="delete_comment"),
    path('edit_comment/', views.edit_comment, name="edit_comment"),
    path('refresh_comments/', views.refresh_comments, name="refresh_comments"),
    path('vote_up/', views.vote_up, name="vote_up"),
    path('vote_down/', views.vote_down, name="vote_down"),
    path('notifications/', views.notifications, name="notifications"),
    path('mark_notification_as_read/', views.mark_notification_as_read, name="mark_notification_as_read"),
]
