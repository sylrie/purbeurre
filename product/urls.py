from django.urls import path

from . import views # import views so we can use them in urls.

app_name='product'

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.Product().results, name='products'),
    path('substitutes/', views.Product().substitutes, name='substitutes'),
    path('food/', views.Product().food, name='food'),
    path('legals/', views.legals, name='legals'),
]