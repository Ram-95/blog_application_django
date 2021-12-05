## Django REST Framework Notes

### What is Serialization ?
* Data serialization is the process of converting structured data to a format that allows sharing or storage of the data in a form that allows recovery of its original structure
* Read it [here](https://docs.python-guide.org/scenarios/serialization/). Notes based on this [Video](https://www.youtube.com/watch?v=B38aDwUpcFc).

In the shell

```python
class BlogSerializer(serializers.ModelSerializer):
    ''' To show Posts data '''
    class Meta:
        model = Blog
        fields = '__all__'


ser = serializers.BlogSerializer()
print(repr(ser))    # will give the fields used in this serializer

Output:

BlogSerializer():
    id = IntegerField(label='ID', read_only=True)
    title = CharField(max_length=100)
    description = CharField(allow_blank=True, allow_null=True, required=False, style={'base_template': 'textarea.html'})
    publish_date = DateTimeField(required=False)
    likes = IntegerField(required=False)
    image = ImageField(allow_null=True, max_length=100, required=False)
    views = IntegerField(required=False)
    slug = SlugField(allow_unicode=False, max_length=255, validators=[<UniqueValidator(queryset=Blog.objects.all())>])
    author = PrimaryKeyRelatedField(queryset=User.objects.all())
```


#### Function Based API Views
```serializers.py```
```python
from blogs.models import Blog, Blog_comments
from rest_framework import serializers

class BlogSerializer(serializers.ModelSerializer):
    ''' To show Posts data '''
    class Meta:
        model = Blog
        fields = '__all__'
```

**Required Imports**
```python
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
```

```views.py```
**Function based API Views**
```python
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
```

**Class Based API Views of the above FBVs using APIView.**

```python
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
```

#### To use authentications like BasicAuthentication, SessionAuthentication and TokenAuthentication
**Use the below inside the API classes for BasicAuthentication, SessionAuthentication**

```python
# If SessionAuthentication is present that is used else BasicAuthentication will be used - That is why a list.
authentication_classes = [SessionAuthentication, BasicAuthentication]
permission_classes = [IsAuthenticated]
```

##### Example:
```python
class BlogGenericAPIView(generics.GenericAPIView, mixins.CreateModelMixin, mixins.ListModelMixin):
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()
    # If SessionAuthentication is present that is used else BasicAuthentication will be used - That is why a list.
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return self.list(request)
    
    def post(self, request):
        return self.create(request)
```

**For TokenAuthentication:**

* Add ```rest_framework.authtoken``` to the ```INSTALLED_APPS``` to the ```settings.py``` file.
* Inside the Class Based API Views. Add this
    ```python
        authentication_classes = [TokenAuthentication]
        permission_classes = [IsAuthenticated]
    ```
* Make migrations and this will create a table called ```Tokens``` where the tokens of users will be stored. By default no tokens are created. We must create the tokens explicitly.
* In Postman, Add this ```Token``` as Authorization and only then we can access the API.

##### Example:
```python
class BlogGenericAPIView(generics.GenericAPIView, mixins.CreateModelMixin, mixins.ListModelMixin):
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return self.list(request)
    
    def post(self, request):
        return self.create(request)
```


**Class Based API Views (CBV) of the above FBVs using GenericAPIViews.**

```python
class BlogGenericAPIView(generics.GenericAPIView, mixins.CreateModelMixin, mixins.ListModelMixin):
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()

    def get(self, request):
        return self.list(request)
    
    def post(self, request):
        return self.create(request)


class BlogGenericDetailAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin):
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()
    lookup_field = 'pk'

    def get(self, request, pk):
        return self.retrieve(request, pk)

    def post(self, request):
        return self.create(request)

    def put(self, request, pk):
        return self.update(request, pk)

    def delete(self, request, pk):
        return self.destroy(request, pk)
```

#### [ModelViewSet](https://www.django-rest-framework.org/api-guide/viewsets/#modelviewset)

The ModelViewSet class inherits from GenericAPIView and includes implementations for various actions, by mixing in the behavior of the various mixin classes.

The actions provided by the ModelViewSet class are .list(), .retrieve(), .create(), .update(), .partial_update(), and .destroy().
**```views.py```**

```python
class PostsViewSet(viewsets.ModelViewSet):
    serializer_class = ViewPostSerializer
    queryset = Blog.objects.all()
```

**```urls.py```**

```python
router = routers.DefaultRouter()
router.register('post', PostsViewSet, basename='post')

urlpatterns = [
    path('viewset/', include(router.urls)),
    path('viewset/<int:pk>/', include(router.urls)),
    ]
```


### Blog Application API Endpoints

- GET ```/api/v1/viewset/users``` - Returns the list of all users registered.

#### Blogposts API Endpoints
- GET ```/api/v1/viewset/posts``` - Returns the list of all posts by all users.
- POST ```/api/v1/viewset/posts``` - Creates a new post. 
    > Data required = ```{"title": "Title", "description": "Description", "author": "Author ID"}```
- GET ```/api/v1/viewset/posts/<id>``` - Returns a post by it's post ID.
- PUT ```/api/v1/viewset/posts/<id>``` - Updates a post by it's post ID.
- DELETE ```/api/v1/viewset/posts/<id>``` - Deletes a post by it's post ID.
- GET ```/api/v1/posts/?username=<username>``` - Returns a list of all posts by a specific user by his username.


#### API Documentation - https://documenter.getpostman.com/view/18647792/UVJhDuVC