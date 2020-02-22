from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from product.models import Product

def index(request):
    
    return render(request,'product/home.html' )

def search_results(request):
    
    return render(request,'product/product.html' )