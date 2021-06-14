from django.db import models
from accounts.models import CustomUser
from django.core.files.storage import default_storage

# Create your models here.
class Document(models.Model):
    file_uid = models.CharField(max_length = 16, null=True)
    file_name = models.CharField(max_length = 255, null=True)
    file_size = models.CharField(max_length = 255, null=True)
    file_document = models.FileField(upload_to='media/uploaded_files/', storage=default_storage)
    uploaded_on = models.DateTimeField(auto_now_add=True, null=True)
    uploaded_by = models.ForeignKey(CustomUser, to_field='uid', on_delete=models.CASCADE)

    def __str__(self):
        return self.file_name

class ConvertedDocument(models.Model):
    file_uid = models.CharField(max_length = 16, null=True)
    file_name = models.CharField(max_length = 255, null=True)
    file_size = models.CharField(max_length = 255, null=True)
    file_document = models.FileField(upload_to='media/converted_files/', storage=default_storage)
    uploaded_on = models.DateTimeField(auto_now_add=True, null=True)
    uploaded_by = models.ForeignKey(CustomUser, to_field='uid', on_delete=models.CASCADE)

    def __str__(self):
        return self.file_name

