from django.urls import path
from . import views

urlpatterns = [
    path("upload/", views.uploadView, name = "upload"),
    path('download/<slug:slug>/', views.downloadView, name='downloads')
]