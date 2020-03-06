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

    def results(self, request, name=None):
        
        if name is not None:
            query = name
        elif request.method == 'POST':
            query = request.POST.get("product-name")
        else:
            query = request.GET.get('name')
    
        self.product_list = search_product(query)
        print(len(self.product_list))
        paginator = Paginator(self.product_list, 9)
        
        page = request.GET.get('page')
        products = paginator.get_page(page)
        
        title = "Recherche"
        
        context = {
            'request': query,
            'products': products,
            'title': title,
            }

        return render(request,'product/product.html', context)

    def substitutes(self, request):
        
        query = request.GET.get('code')

        self.product = select_product(query)
        
        url = "https://world.openfoodfacts.org/product/{}".format(query)
        category = self.product["category"]
        nutrigrade = self.product["nutrigrade"]
        self.substitutes_list = search_substitutes(category, nutrigrade)
        print(len(self.substitutes_list))

        paginator = Paginator(self.substitutes_list, 9)
        
        page = request.GET.get('page')
        products = paginator.get_page(page)

        title = "Substituts"
        
        context = {
            'url': url,
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