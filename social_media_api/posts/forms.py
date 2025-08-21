from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    """
    Form for creating and updating Post objects.
    """
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']


class CommentForm(forms.ModelForm):
    """
    Form for adding a comment to a post.
    """
    class Meta:
        model = Comment
        fields = ["content"]
        labels = {
            'content': 'Comment'
        }
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
        }