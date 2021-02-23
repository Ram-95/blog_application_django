from django import forms
from .models import Blog_comments

class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        # Removes the label for 'content' field
        self.fields['content'].label = False
    
    class Meta:
        model = Blog_comments
        # To override the textarea of crispy-forms to use 3 rows in the textarea
        widgets = {'content': forms.Textarea(attrs={'rows': 3})}
        fields = ['content']
        