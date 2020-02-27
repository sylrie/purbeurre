from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path

from product import views

urlpatterns = [
    path('products/', views.results, name='products'),
    path('substitutes/', views.substitutes, name='substitutes'),
    url(r'^$', views.index),
    url(r'^product/', include('product.urls')),
    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns