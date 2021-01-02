from django import forms
from .models import Blog_comments

class CommentForm(forms.ModelForm):
    class Meta:
        model = Blog_comments
        fields = ['content']