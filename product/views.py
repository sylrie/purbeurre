from django.shortcuts import render, redirect, get_object_or_404
from .models import SavedProduct, FavoriteProduct
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.core.paginator import Paginator

from product.manager_api2 import search_product,  search_substitutes, select_product


def index(request):
    
    return render(request,'product/home.html' )

def legals(request):

    return render(request,'product/legals.html' )

class Product():

    def __init__(self):

        self.product = {}
        self.product_list = []
        self.substitutes_list = []

    def results(self, request):
        title = "Recherche"

        if request.GET.get('page'):
            page = int(request.GET.get('page'))
        else:
            page = 1

        if request.POST.get('product-name'):    

            self.query = request.POST.get("product-name")
            self.product_list = search_product(self.query)
        
        paginator = Paginator(self.product_list, 6)
        products = paginator.page(page)
        
        context = {
            'request': self.query,
            'products': products,
            'title': title,
            }

        return render(request,'product/product.html', context)

    def substitutes(self, request):
        title = "Substituts"
        self.quality = "better"
        if request.GET.get('page'):
            page = int(request.GET.get('page'))
        else:
            page = 1
            
        if request.GET.get('code'):
            query = request.GET.get('code')

            self.product = select_product(query)
            
            self.url = "https://world.openfoodfacts.org/product/{}".format(query)
            category = self.product["category"]
            nutrigrade = self.product["nutrigrade"]

            substitutes = search_substitutes(category, nutrigrade)
            self.substitutes_list = substitutes[0]
            self.quality = substitutes[1]
            
        paginator = Paginator(self.substitutes_list, 6)
        products = paginator.get_page(page)

        context = {
            'url': self.url,
            'product': self.product,
            'products': products,
            'title': title,
            'quality': self.quality,
            }
        
        return render(request,'product/product.html', context)

    def food(self, request):
        title = "Fiche produit"
        query = request.GET.get('code')
        self.product = select_product(query)
        url = "https://world.openfoodfacts.org/product/{}".format(query)

        context = {
            'url': url,
            'title': title,
            'food': self.product,
            }
        return render(request,'product/food.html', context)

    def add_favorite(self, request):

        code = request.GET.get('code')
        product = SavedProduct.objects.filter(code=code)
        
        if not product.exists():
            self.product = select_product(code)

            product = SavedProduct(
                code=self.product["code"],
                name=self.product["name"],
                img=self.product["img"],
                details=self.product["details"],
                nutrigrade=self.product["nutrigrade"],
                )
            product.save() 
        else:
            pass

        new_product = get_object_or_404(SavedProduct, pk=code)
        favorite = FavoriteProduct.objects.filter(user=request.user)
        favorite = favorite.filter(saved_product=code)
        
        if not favorite.exists():
            try:
                new_favorite = FavoriteProduct.objects.create(
                    saved_product=new_product,
                    user=request.user,
                    )
                new_favorite.save()
                message = "Le produit à été ajouté aux favoris"
            except:
                pass
        else:
            message = "Ce produit est déja dans la liste de favoris"
            
        return self.favorites(request, message)
    
    def favorites(self, request, message=None):

        if request.GET.get('page'):
            page = int(request.GET.get('page'))
        else:
            page = 1

        title = "Favoris"
        if message == None:
            message =  ""
        
        favorite = FavoriteProduct.objects.filter(user=request.user).order_by('-date')
        paginator = Paginator(favorite, 6)
        products = paginator.get_page(page)
        
        context = {
            'title': title,
            'message': message,
            'products': products,
            }

        return render(request,'product/favorites.html', context )
