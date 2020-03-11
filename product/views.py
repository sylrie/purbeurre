from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator

from product.manager_api import search_product, search_substitutes, select_product
from .models import SavedProduct, FavoriteProduct



def index(request):
    return render(request, 'product/home.html')

def legals(request):
    return render(request, 'product/legals.html')

class Product():

    """def __init__(self):

        self.product = {}
        self.product_list = []
        self.substitutes_list = []"""

    def results(self, request):
        title = "Recherche"

        if request.GET.get('page'):
            page = int(request.GET.get('page'))
        else:
            page = 1

        if request.POST.get('product-name'):

            self.query = request.POST.get("product-name")
            self.product_list = search_product(self.query)

        paginator = Paginator(self.product_list, 9)
        products = paginator.page(page)

        context = {
            'request': self.query,
            'products': products,
            'title': title,
            }

        return render(request, 'product/product.html', ccontext)

    def substitutes(self, request):
        title = "Substituts"

        if request.GET.get('page'):
            page = int(request.GET.get('page'))
        else:
            page = 1

        if request.GET.get('code'):
            query = request.GET.get('code')

            self.product = select_product(query)
            category = self.product["category"]
            nutrigrade = self.product["nutrigrade"]

            substitutes = search_substitutes(category, nutrigrade)
            self.substitutes_list = substitutes[0]
            self.quality = substitutes[1]

            self.number = len(self.substitutes_list)
        paginator = Paginator(self.substitutes_list, 9)
        products = paginator.get_page(page)

        context = {
            'product': self.product,
            'products': products,
            'title': title,
            'quality': self.quality,
            'number': self.number
            }

        return render(request, 'product/product.html', context)

    def food(self, request):
        title = "Fiche produit"
        if request.GET.get('code'):
            query = request.GET.get('code')
            favorite = False
        if request.GET.get('favorite'):
            query = request.GET.get('favorite')
            favorite = True

        self.product = select_product(query)
        url = "https://world.openfoodfacts.org/product/{}".format(query)

        context = {
            'url': url,
            'title': title,
            'food': self.product,
            'favorite': favorite,
            }
        return render(request, 'product/food.html', context)

    def change_favorite(self, request):
        if not request.user.is_authenticated:
            return redirect('login')

        if request.GET.get('page'):
            return self.favorites(request)

        if request.GET.get('del'):      
            code = request.GET.get('del')

            favorite = FavoriteProduct.objects.filter(user=request.user)
            favorite = favorite.filter(saved_product=code).delete()

            message = "Le produit à été retiré des favoris"

        if request.GET.get('add'):              
            code = request.GET.get('add')
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
                    message = "Le produit à été ajouté aux favoris !"
                except:
                    pass
            else:
                message = "Tu avais déjà ce produit en favoris"

        return self.favorites(request, message, code=code)

    def favorites(self, request, message=None, code=None):

        if request.GET.get('page'):
            page = int(request.GET.get('page'))
        else:
            page = 1

        title = "Favoris"

        if message == "Tu avais déjà ce produit en favoris":
            favorite = FavoriteProduct.objects.filter(user=request.user)
            favorite = favorite.filter(saved_product=code)
        else:
            favorite = FavoriteProduct.objects.filter(user=request.user).order_by('-date')
        paginator = Paginator(favorite, 9)
        products = paginator.get_page(page)

        number = len(favorite)
        context = {
            'title': title,
            'message': message,
            'code': code,
            'products': products,
            'number': number,
            }

        return render(request, 'product/favorites.html', context )
