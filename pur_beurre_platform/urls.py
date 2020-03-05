from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path


from product import views as product
from users import views as users

urlpatterns = [

    #PRODUCT APP
    path('', product.index, name='index'),
    path('legals/', product.legals, name='legals'),
    path('products/', product.Product().results, name='products'),
    path('substitutes/', product.Product().substitutes, name='substitutes'),
    path('food/', product.Product().food, name='food'),
    
    #USERS APP
    path('register/', users.register, name='register'),
    path('login/', users.login, name='login'),
    path('logout/', users.logout, name='logout'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns