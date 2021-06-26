from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from .forms import CustomUserCreationForm
from django.http import HttpResponse
from django.contrib import messages

# Create your views here.
def welcomeView(request):
    if request.user.is_authenticated:
        return redirect('upload')
    return render(request, 'welcome.html')

def loginView(request):
    if request.method == 'POST':
        usr_email = request.POST['email']
        usr_password = request.POST['password']
        user = authenticate(email = usr_email, password = usr_password)
        if user is not None:
            login(request, user)
            return redirect('upload')
        else:
            messages.error(request, 'Incorrect email or password!')
            return redirect('login')
    else:
        if request.user.is_authenticated:
            return redirect('upload')
        return render(request, 'accounts/login.html')

def logoutView(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('login')

def registerView(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            print("created instance")
            instance.uid = get_random_string(length=16)
            print("generated uid for instance")
            instance.save()
            print("gsaved the record")
            print("Record added successfully!")
            messages.success(request, 'Account created successfully!')
            return redirect('login')
        else:
            messages.error(request, 'Could not create account!')
            messages.warning(request, 'Please make sure that all fields are filled correctly!')
            return redirect('register')
    else:
        if request.user.is_authenticated:
            return redirect('upload')
        form = CustomUserCreationForm()
        return render(request, 'accounts/register.html', {
            'form':form
        })
