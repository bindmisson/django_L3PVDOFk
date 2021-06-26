from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from functions import views as functions_view

from . import views

urlpatterns = [
    path("", views.welcomeView, name = "welcome"),
    path("login/", views.loginView, name = "login"),
    path("logout/", views.logoutView, name = "logout"),
    path("register/", views.registerView, name = "register"),
    path('download/<slug:slug>/', functions_view.downloadView, name='download'),
    path("upload/", functions_view.uploadView, name = "upload"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
