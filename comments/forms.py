#comments/forms

from django import forms
from .models import PostComment

class PostForm(forms.ModelForm):
    class Meta:
        model = PostComment
        # exclude = ['author', 'updated', 'created', ]
        fields = ['author', 'text']