from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('create_post/', views.create_post, name="create_post"),
    path('post/<int:pk>/', views.view_post, name="view_post"),
    path('vote_up/', views.vote_up, name="vote_up"),
    path('vote_down/', views.vote_down, name="vote_down"),
]
