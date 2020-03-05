from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .forms import UserRegisterForm
from django.contrib.auth import authenticate


from django.contrib.auth.models import User

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            #username = form.cleaned_data.get('username')
            #messages.success(request, "Votre compte a bien été créé, {}!".format(username))

            return redirect('login')
    else:
        form = UserRegisterForm()
        users = User.objects.all()
        for user in users:
            print(user.username)
            print(user.email)
       
    return render(request, 'users/register.html')
    
def login(request):

    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")
        print(email)
        print(password)
        user = authenticate(email=email, password=password)
        
        if user is not None:
            print("ok")
            
        else:
            print("raté")
            
        return redirect('index')
    
    else:
        
        return render(request,'users/login2.html')
            
def logout(request):

    return render(request,'users/logout.html' )