from http.client import SERVICE_UNAVAILABLE
from django.db.models import query
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework.fields import SerializerMethodField
from blogs.models import Blog, Blog_comments
from .serializers import UserSerializer, BlogSerializer, ViewPostSerializer
from rest_framework import serializers, viewsets, generics
from rest_framework.exceptions import NotFound
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view


class UserViewSet(viewsets.ModelViewSet):
    '''
    API endpoint to view the users data by username
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


@api_view(['GET', 'POST'])
def blog_list(request):
    blogs = Blog.objects.all()
    if request.method == 'GET':
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'POST'])
def blog_detail(request, pk):
    try:
        blog = Blog.objects.get(pk=pk)
    except Blog.DoesNotExist:
        raise NotFound()
        # return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    serializer = BlogSerializer(blog)
    if request.method == 'GET':
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = BlogSerializer(blog, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'POST':
        serializer = BlogSerializer(blog, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogViewSet(generics.ListAPIView):
    '''
    API endpoint to view the posts data by username.
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
