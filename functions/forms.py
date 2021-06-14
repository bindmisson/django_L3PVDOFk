from django import forms
from .models import Document

class FileUploadForm(forms.ModelForm):
    file_document = forms.FileField(widget=forms.FileInput(attrs={'name':'uploaded_file'}))

    class Meta:
        model = Document
        fields = ('file_document',)