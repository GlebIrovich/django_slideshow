# carousel/forms

from django import forms

class DocumentForm(forms.Form):
    title = forms.CharField(max_length=100, label= 'Select a name')
    docfile = forms.FileField(label = 'Select a file') 