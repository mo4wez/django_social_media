from django import forms

from .models import Post

class PostCreateAndUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body',]
