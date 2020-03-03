from django.shortcuts import render

# Create your views here.

def create_acount(request):

    return render(request,'users/create.html')

def login(request):

    return render(request,'users/login.html' )