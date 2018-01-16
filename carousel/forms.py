# carousel/forms

from django import forms
from .models import PostComment


class DocumentForm(forms.Form):
    title = forms.CharField(max_length=100, label= 'Select a name')
    docfile = forms.FileField(label = 'Select a file')

class PostForm(forms.ModelForm):
    class Meta:
        model = PostComment
        # exclude = ['author', 'updated', 'created', ]
        fields = ['author', 'text']