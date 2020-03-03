from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path

from product import views as product
from users import views as users

urlpatterns = [
    path('', product.index, name='index'),
    path('products/', product.Product().results, name='products'),
    path('substitutes/', product.Product().substitutes, name='substitutes'),
    path('food/', product.Product().food, name='food'),
    path('create/', users.create_acount, name='create'),
    path('login/', users.login, name='login'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns