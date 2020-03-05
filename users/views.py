from django.shortcuts import render, redirect
from django.template import loader
from .forms import UserRegisterForm
from django.contrib.auth import authenticate


from django.contrib.auth.models import User

# Create your views here.

def register(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        print("oups {}".format(email))
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            #username = form.cleaned_data.get('username')
            #messages.success(request, 'Votre compte a bien été créé, {}! Vous pouvez vous connecter.'.format(username))

            return redirect('login')
    else:
        form = UserRegisterForm()
        users = User.objects.all()
        for user in users:
            print(user.username)
        

    context = {
            'form': form,
            }
   
    return render(request, 'users/register.html', context)
    

def login(request):

    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")
        print(email)
        print(password)
        user = authenticate(email=email, password=password)
        
        if user is not None:
            print("raté")
            
        else:
            print("ok")
            
        return redirect('index')
    
    else:
        
        
        return render(request,'users/register.html')
            
            



def logout(request):

    return render(request,'users/logout.html' )