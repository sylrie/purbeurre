from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

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
    
    context = {
        'products': products,
        }

    return render(request,'product/product.html', context)

def substitutes(request):
    
    query = request.GET.get('code')
    print(query)
    product = select_product(query)
    category = product["category"]
    substitutes = search_substitutes(category)
    
    context = {
        'product': product,
        'products': substitutes,
        }

    return render(request,'product/product.html', context)