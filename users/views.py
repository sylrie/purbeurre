from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .forms import UserRegisterForm
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        
        if form.is_valid():
            form.save()

            return redirect('login')
    
        else:
            print("register problem")
            return redirect('register')
                  
    return render(request, 'users/register.html')
    
def login (request):
    return render(request,'users/login.html' )     

@login_required
def logout(request):
    return render(request,'users/logout.html' )

@login_required
def profile(request):
    return render(request, 'users/profile.html')