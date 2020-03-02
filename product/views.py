from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.core.paginator import Paginator

from product.manager_api2 import search_product,  search_substitutes, select_product
from .models import Product

def index(request):
    
    return render(request,'product/home.html' )


def results(request, name=None):
    
    if name is not None:
        query = name
    elif request.method == 'POST':
        query = request.POST.get("product-name")
    else:
        query = request.GET.get('name')   
  
    products = search_product(query)
    #paginator = Paginator(products, 9)
    #products = paginator.page(paginator.num_pages)
    
    context = {
        'products': products,
        'request': query,
        }

    return render(request,'product/product.html', context)

def substitutes(request):
    
    query = request.GET.get('code')

    product = select_product(query)
    url = "https://world.openfoodfacts.org/product/{}".format(query)
    category = product["category"]
    nutrigrade = product["nutrigrade"]
    

    substitutes = search_substitutes(category, nutrigrade)
    
    #paginator = Paginator(substitutes, 11)
    #substitutes = paginator.page(paginator.num_pages)

    context = {
        'url': url,
        'product': product,
        'products': substitutes,
        }

    return render(request,'product/product.html', context)