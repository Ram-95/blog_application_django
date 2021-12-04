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