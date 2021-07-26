from django.contrib.auth.models import User
from blogs.models import Blog
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'


class ViewPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'
