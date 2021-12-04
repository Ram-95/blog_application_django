## Django REST Framework Notes

### What is Serialization ?
* Data serialization is the process of converting structured data to a format that allows sharing or storage of the data in a form that allows recovery of its original structure
* Read it [here](https://docs.python-guide.org/scenarios/serialization/)
In the shell

```python
class BlogSerializer(serializers.ModelSerializer):
    ''' To show Posts data '''
    class Meta:
        model = Blog
        fields = '__all__'

# In the shell
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