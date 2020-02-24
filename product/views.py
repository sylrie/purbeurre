from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Product

def index(request):
    
    return render(request,'product/home.html' )

def search_results(request):

    product = Product.objects.all()
    #formatted_food = ["<li>{}</li>".format(food) for food in food]
    #message = """<ul>{}</ul>""".format("\n".join(formatted_food))
    context = {'product': product}
    #return HttpResponse(render(context, 'product/product.html'))

    return render(request,'product/product.html', context )