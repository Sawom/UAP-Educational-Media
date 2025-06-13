from django import forms
from App_Posts.models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['image', 'caption',]


from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Add a comment...'}),
        }
