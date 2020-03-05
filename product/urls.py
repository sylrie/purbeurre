from django.urls import path
from . import views

app_name='product'

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.Product().results, name='products'),
    path('substitutes/', views.Product().substitutes, name='substitutes'),
    path('food/', views.Product().food, name='food'),
    path('legals/', views.legals, name='legals'),
]