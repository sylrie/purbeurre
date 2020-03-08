from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required


def register(request):
    title = "Inscription"
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre compte a bien été créé,<br> Vous pouvez vous connecter.')
            return redirect('login')
            
    else:
        form = UserRegisterForm()
        
 
    return render(request, 'users/register.html', {'form': form, 'title': title})
    
def login (request):
    
    return render(request,'users/login.html', {'title': "Connexion"} )     

@login_required
def logout(request):
    return render(request,'users/logout.html', {'title': "Déconnexion"} )

@login_required
def profile(request):
    
    return render(request, 'users/profile.html', {'title': "Profil"})