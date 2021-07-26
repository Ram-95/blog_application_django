from django.db.models import query
from django.shortcuts import render
from django.contrib.auth.models import User
from blogs.models import Blog
from .serializers import UserSerializer, BlogSerializer, ViewPostSerializer
from rest_framework import viewsets, generics
from rest_framework.exceptions import NotFound


class UserViewSet(viewsets.ModelViewSet):
    '''
    API endpoint to view the users
    '''
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.all()
        username = self.request.query_params.get('username')
        if username is not None:
            queryset = queryset.filter(username=username)
            return queryset
        else:
            raise NotFound()


class BlogViewSet(generics.ListAPIView):
    '''
    API endpoint to view the posts of a user.
    '''
    serializer_class = BlogSerializer

    def get_queryset(self):
        queryset = Blog.objects.all()
        username = self.request.query_params.get('username')
        if username is not None:
            queryset = queryset.filter(author__username=username)
            if queryset.exists():
                return queryset
        raise NotFound()
        


class ViewPostViewSet(generics.ListAPIView):
    '''
    API endpoint to view a specific post by it's id
    '''
    serializer_class = ViewPostSerializer

    def get_queryset(self):
        queryset = Blog.objects.all()
        post_id = self.request.query_params.get('post_id')
        if post_id is not None:
            queryset = queryset.filter(id=post_id)
            if queryset.exists():
                return queryset
        raise NotFound()
