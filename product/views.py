from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.core.paginator import Paginator

from product.manager_api2 import search_product,  search_substitutes, select_product


def index(request):
    
    return render(request,'product/home.html' )
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
        #paginator = Paginator(products, 9)
        #products = paginator.page(paginator.num_pages)
        
        context = {
            'products': self.product_list,
            'request': query,
            }

        return render(request,'product/product.html', context)

    def substitutes(self, request):
        
        query = request.GET.get('code')

        self.product = select_product(query)
        url = "https://world.openfoodfacts.org/product/{}".format(query)
        category = self.product["category"]
        nutrigrade = self.product["nutrigrade"]
        

        self.substitutes_list = search_substitutes(category, nutrigrade)

        #paginator = Paginator(substitutes, 11)
        #substitutes = paginator.page(paginator.num_pages)

        context = {
            'url': url,
            'product': self.product,
            'products': self.substitutes_list,
            }

        return render(request,'product/product.html', context)

    def food(self, request):

        query = request.GET.get('code')
        print(query)
        self.product = select_product(query)
        url = "https://world.openfoodfacts.org/product/{}".format(query)
        for product in self.product_list:
            if product.get("code") == query:
                self.product = product
                break
            else:
                pass
        print(self.product["brand_link"])    
        context = {
            'url': url,
            'food': self.product,
            }
        return render(request,'product/food.html', context)
