""" Views for users app """

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from product.models import FavoriteProduct
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

def register(request):
    """ account creation """

    title = "Inscription"
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Ton compte a bien été créé, tu peux te connecter.')
            
            return redirect('login')
            
    else:
        form = UserRegisterForm()
    
    logger.info('New Visit', exc_info=True, extra={
        # Optionally pass a request and we'll grab any information we can
        'request': request,
    })
    return render(request, 'users/register.html', {'form': form, 'title': title})

def login(request, message=None):
    """ Authentification """
    if message:
        return render(request,'users/login.html', {'message': message})
    else:
        return render(request,'users/login.html')     

@login_required
def update_profile(request):
    print('1')
    if request.method == 'POST':
        user = request.user
        new_password = request.POST.get("new_password")
        print(new_password)
        try:
            user.set_password(new_password)
            user.save()
            message = "Le mot de passe à été modifié !"
            return redirect('profile')
        except:
            message = "raté"
              
    else:
        print('else')
        message = None

    context = {
        'message': message
    }

    return render(request, 'users/profile.html', context)
 
@login_required
def logout(request):

    return render(request,'users/logout.html', {'title': "Déconnexion"})

@login_required
def profile(request):
    """ acces to user profile """

    name = str(request.user).capitalize()
    favorites = len(FavoriteProduct.objects.filter(user=request.user))
    
    if request.method == 'POST':
        user = request.user
        new_password = request.POST.get("new_password")
        print(new_password)
        try:
            user.set_password(new_password)
            user.save()
            message = "Le mot de passe à été modifié !"
            return redirect('profile')
        except:
            message = "raté"
              
    else:
        
        message = None

    context = {
        'title': 'profil',
        'name': name,
        'favorites': favorites,
        'message': message
    }

    return render(request, 'users/profile.html', context)
