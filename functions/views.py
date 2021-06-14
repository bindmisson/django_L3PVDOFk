from accounts import urls

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import render,redirect
from django.utils.crypto import get_random_string
from accounts.models import CustomUser
from django.core.files.storage import default_storage
from wsgiref.util import FileWrapper
from django.core.files.storage import FileSystemStorage
from app.settings import TEMP_ROOT, TEMP_URL


import pandas as pd
import os
import io
import csv

from app import settings
from .models import Document, ConvertedDocument
from .core import analysis
from django.contrib import messages


temp_storage = FileSystemStorage(location=TEMP_ROOT, base_url=TEMP_URL)

# Create your views here.
@login_required(login_url='login')
def uploadView(request):
    if(request.method == 'POST'):
        records = Document.objects.filter(uploaded_by_id=request.user.uid)
        user = CustomUser.objects.get(uid=request.user.uid)

        uploaded_file = request.FILES['upload_field']

        generated_uid = get_random_string(16)
        generated_name = generated_uid+".csv"
        actual_name = uploaded_file.name

        # Block to save converted file
        try:
            csv_response = analysis(uploaded_file).content.decode('utf-8')
        except Exception as e:
            messages.error(request, 'There was an error processing the file please make sure that the file uploaded is in the correct format!')
            return redirect('upload')
        csv_response = csv_response.replace('\r\n', '\n')
        #return csv_response
        #return HttpResponse(csv_response)
        f = temp_storage.open('temp.csv', 'w')
        f.write(csv_response)
        f.close()
         

        #HttpResponse(csv_response)

        #return csv_response
        

        converted_file = temp_storage.open('temp.csv')

        converted_file.name = generated_name

        converted_document = ConvertedDocument()
        converted_document.file_uid = generated_uid
        converted_document.file_name = "converted_"+actual_name
        converted_document.file_size = converted_file.size
        converted_document.file_document = converted_file
        converted_document.uploaded_by = user
        converted_document.save()


        # Block to save uploaded file
        uploaded_file.name = generated_name
        
        document = Document()
        document.file_uid = generated_uid
        document.file_name = actual_name
        document.file_size = uploaded_file.size
        document.file_document = uploaded_file
        document.uploaded_by = user
        document.save()
        messages.success(request, 'File uploaded successfully!')
        return redirect('upload')
    else:
        records = Document.objects.filter(uploaded_by_id=request.user.uid).order_by('-id')
        return render(request, 'functions/upload.html', {'records':records})
    

def downloadView(request, slug):
    converted_document = ConvertedDocument.objects.get(file_uid=slug)
    actual_name = converted_document.file_name

    file_name = slug+".csv"
    file_partial_path = "converted_files\\"+file_name
    #file_path = os.path.join(settings.MEDIA_ROOT, file_partial_path)
    file_path = default_storage.open('media/converted_files/'+file_name)
    # with open(file_path, 'r') as fh:
    #     response = HttpResponse(fh.read(), content_type='text/csv')
    #     response['Content-Disposition']= 'attachment; filename="{}"'.format(actual_name)
    #     return response
    # raise Http404
    response = HttpResponse(file_path.read(), content_type='text/csv')
    response['Content-Disposition']= 'attachment; filename="{}"'.format(actual_name)
    return response
