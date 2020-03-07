from django.shortcuts import render
from django.http import HttpResponse
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

            self.substitutes_list = search_substitutes(category, nutrigrade)
 
        paginator = Paginator(self.substitutes_list, 6)
        products = paginator.get_page(page)

        context = {
            'url': self.url,
            'product': self.product,
            'products': products,
            'title': title
            }

        return render(request,'product/product.html', context)

    def food(self, request):

        query = request.GET.get('code')
        self.product = select_product(query)
        url = "https://world.openfoodfacts.org/product/{}".format(query)
        for product in self.product_list:
            if product.get("code") == query:
                self.product = product
                break
            else:
                pass
    
        context = {
            'url': url,
            'food': self.product,
            }
        return render(request,'product/food.html', context)

    def favorites(self, request):

        title = "Favorites"
        context = {
            'title': title,
            }

        return render(request,'product/favorites.html', context )