from django.urls import path

from . import views # import views so we can use them in urls.

app_name='product'

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.results, name='products'),
    path('substitutes/', views.substitutes, name='substitutes'),
]