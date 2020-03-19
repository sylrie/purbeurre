from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator

import re
from product.manager_api import ProductData as search
from product.update_data import UpdateData
from users import views
from .models import FavoriteProduct, Products


def index(request):
    return render(request, 'product/home.html')

def legals(request):
    return render(request, 'product/legals.html')

     
class Product():

    def results(self, request):
        title = "Pur Beurre - Recherche"
        error = None
        self.qty = None
        
        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1
        
        if request.POST.get('product-name'):
            self.base_product = "Pur Beurre"
            query = request.POST.get("product-name")
            # Remove space end and start
            user_request = re.sub(r"( )+$", "", query)
            self.user_request = re.sub(r"^( )+", "", user_request)

            self.product_list = Products.objects.filter(name__icontains=self.user_request).order_by("-name")

            self.qty = len(self.product_list)
            
        elif request.GET.get('off-name'):
            self.base_product = "Open Food Facts"
            self.user_request = request.GET.get("off-name")
            try:
                self.product_list = search().search_product(self.user_request)
            except:
                error ="Oups, nous n'arrivons pas à contacter Open Food Facts"

        paginator = Paginator(self.product_list, 9)
        try:
            self.products = paginator.page(page)
        except:
            self.products = paginator.page(paginator.num_pages)

        context = {
            'request': self.user_request,
            'products': self.products,
            'number': self.qty,
            'title': title,
            'error': error,
            'base_product': self.base_product,
            }

        return render(request, 'product/product.html', context)

    def substitutes(self, request):
        title = "Pur Beurre - Substituts"
        error = None
        nutrigrades = [
            'a',
            'b',
            'c',
            'd',
            'e'
        ]

        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1

        if request.GET.get('code'):
            self.query = request.GET.get('code')
        elif request.GET.get('off-code'):   
            self.query = request.GET.get('off-code')

        try:
            self.product = Products.objects.get(pk=query)
            category = self.product.category
            nutrigrade = self.product.nutrigrade

        except:
            pass
        
        try:
            self.product = search().select_product(self.query)
            category = self.product["category"]
            nutrigrade = self.product["nutrigrade"]

        except:
            pass

        if request.GET.get('code'):
            self.base_substitute = "Pur Beurre"
            try:
                self.base_substitute = "Pur Beurre"
                self.query = request.GET.get('code')
                self.substitutes_list = Products.objects.filter(category=category)
                
                for grade in nutrigrades:
                    self.substitutes_list = self.substitutes_list.filter(nutrigrade=grade).order_by("-nutrigrade")

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
                pass

        elif request.GET.get('off-code'):
            self.base_substitute = "Open Food Facts"
            try:
                self.base_substitute = "Open Food Facts"
                self.query = request.GET.get('off-code')
                substitutes = search().search_substitutes(category, nutrigrade)
                self.substitutes_list = substitutes[0]
                index = 0
                for product in self.substitutes_list:
                    if product["code"] == self.query:
                        del self.substitutes_list[index]
                    else:
                        index += 1

                self.quality = substitutes[1]
            except:
                error ="Oups, nous n'arrivons pas à contacter Open Food Facts"
        
        paginator = Paginator(self.substitutes_list, 9)
        try:
            self.products = paginator.page(page)
        except:
            self.products = paginator.page(paginator.num_pages)
        
        self.number = len(self.substitutes_list)

        context = {
            'code': self.query,
            'product': self.product,
            'products': self.products,
            'title': title,
            'quality': self.quality,
            'number': self.number,
            'error': error,
            'base_product': self.base_substitute,
            }

        return render(request, 'product/product.html', context)

    def food(self, request):
        title = "Pur Beurre - Fiche produit"
        
        if request.GET.get('code'):
            query = request.GET.get('code')
            favorite = False
        if request.GET.get('favorite'):
            query = request.GET.get('favorite')
            favorite = True

        try:
            self.product = Products.objects.get(pk=query)
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
       
        if not request.user.is_authenticated:
            return redirect('login')

        if request.GET.get('del'):      
            code = request.GET.get('del')
            
            favorite = FavoriteProduct.objects.filter(user=request.user)
            favorite = favorite.filter(saved_product=code).delete()
            
            del_product = get_object_or_404(Products, pk=code)
            del_product.favorite -= 1
            del_product.save()
            
            message = "Le produit à été retiré des favoris"

        elif request.GET.get('add'):          
            code = request.GET.get('add')
            product = Products.objects.filter(code=code)
    
            if not product.exists():
                product = search().select_product(code)
                try:
                    new = Products(
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

            new_product = get_object_or_404(Products, pk=code)
            favorite = FavoriteProduct.objects.filter(user=request.user)
            favorite = favorite.filter(saved_product=code)

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
        title = "Pur Beurre - Favoris"

        try:
            page = int(request.GET.get('page', '1'))
        except ValueError:
            page = 1

        if message == "Tu avais déjà ce produit en favoris":
            favorite = FavoriteProduct.objects.filter(user=request.user)
            favorite = favorite.filter(saved_product=code)
        else:
            favorite = FavoriteProduct.objects.filter(user=request.user).order_by('-date')
        
        number = len(favorite)
        paginator = Paginator(favorite, 9)
        products = paginator.get_page(page)

        context = {
            'title': title,
            'message': message,
            'code': code,
            'products': products,
            'number': number,
            }

        return render(request, 'product/favorites.html', context )

