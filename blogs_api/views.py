from http.client import SERVICE_UNAVAILABLE
from django.db.models import query
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework.fields import SerializerMethodField
from blogs.models import Blog, Blog_comments
from .serializers import UserSerializer, BlogSerializer, ViewPostSerializer
from rest_framework import serializers, viewsets, generics, mixins
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated


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


######################### Function based API Views ######################################
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


@api_view(['GET', 'PUT', 'DELETE'])
def blog_detail(request, pk):
    """API to GET, PUT and DELETE a blogpost."""
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
    elif request.method == 'DELETE':
        blog.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

######################### END of Function based API Views ######################################

######################### CBV APIViews of Function based API Views above. ######################################


class BlogAPIView(APIView):
    """Class Based View similar to blog_list FBV above."""

    def get(self, request):
        blogs = Blog.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)


class BlogDetailAPIView(APIView):
    """Class Based View of blog_detail FBV above."""

    def get_object(self, pk):
        try:
            blog = Blog.objects.get(pk=pk)
            return blog
        except Blog.DoesNotExist:
            raise NotFound()

    def get(self, request, pk):
        blog = self.get_object(pk)
        serializer = BlogSerializer(blog)
        return Response(serializer.data)

    def put(self, request, pk):
        blog = self.get_object(pk)
        serializer = BlogSerializer(blog, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        blog = self.get_object(pk)
        blog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
######################### End of CBV APIViews of Function based API Views above. ###########################

############################ CBV Generic APIViews ###################################
class BlogGenericAPIView(generics.GenericAPIView, mixins.CreateModelMixin, mixins.ListModelMixin):
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()
    # If SessionAuthentication is present that is used else BasicAuthentication will be used - That is why a list.
    #authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return self.list(request)
    
    def post(self, request):
        return self.create(request)


class BlogGenericDetailAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin):
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()
    lookup_field = 'pk'
    # If SessionAuthentication is present that is used else BasicAuthentication will be used - That is why a list.
    #authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def get(self, request, pk):
        return self.retrieve(request, pk)

    def post(self, request):
        return self.create(request)

    def put(self, request, pk):
        return self.update(request, pk)

    def delete(self, request, pk):
        return self.destroy(request, pk)

############################ END of CBV Generic APIViews ###################################


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
