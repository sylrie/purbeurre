""" Manage views for product app """
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

import re
from product.manager_api import ProductData as search
from product.update_data import UpdateData
from users import views
from .models import FavoriteProduct, BaseProduct

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


def index(request):
    """ Home page """
    return render(request, 'product/home.html')

def legals(request):
    """ Legals page """
    return render(request, 'product/legals.html')
     
class Product():
    """ Manage products views """
    
    def results(self, request):
        """ Display search results from database or Off """

        title = "Pur Beurre - Recherche"
        error = None
        self.qty = None
        
        # search in database
        if request.POST.get('product-name'):
            self.base_product = "Pur Beurre"
            query = request.POST.get("product-name")
            
            # Remove space end and start
            user_request = re.sub(r"( )+$", "", query)
            self.user_request = re.sub(r"^( )+", "", user_request)

            self.product_list = BaseProduct.objects.filter(name__icontains=self.user_request).order_by("-name")[:18]

            self.qty = len(self.product_list)

        # search in off API    
        elif request.GET.get('off-name'):
            self.product_list = []
            self.base_product = "Open Food Facts"
            self.user_request = request.GET.get("off-name")
            try:
                product_list = search().search_product(self.user_request)
                count = 0
                for food in product_list:
                    self.product_list.append(food)
                    count += 1
                    if count == 18:
                        break
            except:
                error ="Oups, nous n'arrivons pas à contacter Open Food Facts"
        
        self.qty = len(self.product_list)
 
        context = {
            'request': self.user_request,
            'products': self.product_list,
            'number': self.qty,
            'title': title,
            'error': error,
            'base_product': self.base_product,
        }
        
        logger.info('New Search', exc_info=True, extra={
        # Optionally pass a request and we'll grab any information we can
        'request': request,
        })
        return render(request, 'product/product.html', context)

    def substitutes(self, request):
        """ Display substitutes from database or Off """

        title = "Pur Beurre - Substituts"
        error = None
        nutrigrades = [
            'a',
            'b',
            'c',
            'd',
            'e'
        ]

        # Get product code
        if request.GET.get('code'):
            self.query = request.GET.get('code')
        elif request.GET.get('off-code'):   
            self.query = request.GET.get('off-code')

        # search product in database
        try:
            self.product = BaseProduct.objects.get(pk=query)
            category = self.product.category
            nutrigrade = self.product.nutrigrade
        except:
            pass

        # search product in off API
        try:
            self.product = search().select_product(self.query)
            category = self.product["category"]
            nutrigrade = self.product["nutrigrade"]
        except:
            pass

        # search substitutes in database
        if request.GET.get('code'):
            self.base_substitute = "Pur Beurre"
            try:
                self.base_substitute = "Pur Beurre"
                self.query = request.GET.get('code')
                self.substitutes_list = BaseProduct.objects.filter(category=category)
                self.substitutes_list = self.substitutes_list.exclude(code=self.query)
                
                for grade in nutrigrades:
                    self.substitutes_list = self.substitutes_list.filter(nutrigrade=grade).order_by("-nutrigrade")[:18]

                    if len(self.substitutes_list) > 0:
                        if grade == nutrigrade:
                            self.quality = "equal"
                        else:
                            self.quality = "better"
                        break
                    else:
                        self.quality = None
                    if grade == nutrigrade:
                        break
            except:
                self.quality = None
                self.substitutes_list = []

        # search substitutes in off API
        elif request.GET.get('off-code'):
            self.substitutes_list = []
            self.base_substitute = "Open Food Facts"
            try:
                self.base_substitute = "Open Food Facts"
                self.query = request.GET.get('off-code')
                substitutes = search().search_substitutes(category, nutrigrade)
                substitutes_list = substitutes[0]
                count = 0
                for product in substitutes_list:
                    if product["code"] == self.query:
                        pass
                    else:
                        self.substitutes_list.append(product)
                        count += 1
                    if count == 18:
                        break
                    
                self.quality = substitutes[1]
            except:
                self.quality = None
                self.substitutes_list = []
                error ="Oups, nous n'arrivons pas à contacter Open Food Facts"
        
        self.number = len(self.substitutes_list)

        context = {
            'code': self.query,
            'product': self.product,
            'products': self.substitutes_list,
            'title': title,
            'quality': self.quality,
            'number': self.number,
            'error': error,
            'base_product': self.base_substitute,
            }

        return render(request, 'product/product.html', context)

    def food(self, request):
        """ Display details off the selected product from database or Off """

        title = "Pur Beurre - Fiche produit"
        
        # Get product code
        if request.GET.get('code'):
            query = request.GET.get('code')
            favorite = False
        if request.GET.get('favorite'):
            query = request.GET.get('favorite')
            favorite = True

        # search product in database or off API
        try:
            self.product = BaseProduct.objects.get(pk=query)
            base = "Pur Beurre"
        except:
            self.product = search().select_product(query)
            base = "Open Food Facts"

        url = "https://world.openfoodfacts.org/product/{}".format(query)

        context = {
            'url': url,
            'title': title,
            'food': self.product,
            'favorite': favorite,
            'base_product': base,
            }

        return render(request, 'product/food.html', context)

    def change_favorite(self, request):
        """ Manage favorites """

        # Check if user is logged
        if not request.user.is_authenticated:
            return redirect('login')

        # delete favorite
        if request.GET.get('del'):      
            code = request.GET.get('del')
            
            favorite = FavoriteProduct.objects.filter(user=request.user)
            favorite = favorite.filter(saved_product=code).delete()
            
            del_product = get_object_or_404(BaseProduct, pk=code)
            del_product.favorite -= 1
            del_product.save()
            
            message = "Le produit à été retiré des favoris"

        # add favorite
        elif request.GET.get('add'):          
            code = request.GET.get('add')
            product = BaseProduct.objects.filter(code=code)
    
            # Check if product is in databse
            if not product.exists():
                product = search().select_product(code)
                try:
                    new = BaseProduct(
                        code = product["code"],
                        category = product["category"],
                        name = product["name"],
                        img = product["img"],
                        details = product["details"],
                        brand = product["brand"],
                        stores = product["stores"],
                        nutrigrade = product["nutrigrade"],
                        ingredients = product["ingredients"],
                        fat = product["fat"],
                        saturated_fat = product["saturated_fat"],
                        salt = product["salt"],
                        sugar = product["sugar"],
                        level_fat = product["level_fat"],
                        level_saturated_fat = product["level_saturated_fat"],
                        level_salt = product["level_salt"],
                        level_sugar = product["level_sugar"],
                        nova = product["nova"]
                    )
                    new.save()
                except:
                    message = "Oups... Le produit n'a pas été ajouté aux favoris !"
                    return self.favorites(request, message=message, code=code)

            new_product = get_object_or_404(BaseProduct, pk=code)
            favorite = FavoriteProduct.objects.filter(user=request.user)
            favorite = favorite.filter(saved_product=code)

            # Check if product is already a favorite
            if not favorite.exists():
                try:
                    new_product.favorite += 1
                    new_product.save()
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

        else:
            return self.favorites(request)

        return self.favorites(request, message=message, code=code)
    
    def favorites(self, request, message=None, code=None):
        """ Display favorites """

        title = "Pur Beurre - Favoris"

        # page for paginator
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1

        # find Top 6 users favorites
        if request.GET.get('top'):
            message = "Top 6 des utilisateurs"
            favorite = BaseProduct.objects.all()
            favorite = favorite.exclude(favorite=0).order_by('-favorite')[:6]
            title = 'Pur Beurre - Top 6'

        # find favorites
        else:        
            if message == "Tu avais déjà ce produit en favoris":
                favorite = FavoriteProduct.objects.filter(user=request.user)
                favorite = favorite.filter(saved_product=code)
            else:
                favorite = FavoriteProduct.objects.filter(user=request.user).order_by('-date')
        
        number = len(favorite)
        paginator = Paginator(favorite, 6)
        products = paginator.get_page(page)
        
        context = {
            'title': title,
            'message': message,
            'code': code,
            'products': products,
            'number': number,
            }

        return render(request, 'product/favorites.html', context )
