from django.contrib.auth.models import User
from blogs.models import Blog, Blog_comments
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    ''' To show User data '''
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class UserSerializerPOST(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class BlogSerializer(serializers.ModelSerializer):
    ''' To show Posts data '''
    class Meta:
        model = Blog
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    ''' To show Comments data '''
    class Meta:
        model = Blog_comments
        fields = '__all__'


class ViewPostSerializer(serializers.ModelSerializer):
    ''' To show a specific post along with comments data '''
    # Use the CommentSerilizer to show comments as nested json
    # Refer: https://www.django-rest-framework.org/api-guide/relations/#nested-relationships
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Blog
        fields = '__all__'
