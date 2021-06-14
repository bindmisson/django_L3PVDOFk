from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=64, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First name'}))
    last_name = forms.CharField(max_length=64, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last name'}))
    email = forms.CharField(max_length=128, widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'}))
    username = forms.CharField(max_length=64, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username'}))
    password1 = forms.CharField(max_length=64, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))
    password2 = forms.CharField(max_length=64, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Confirm password'}))

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'username']
