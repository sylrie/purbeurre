
from django.urls import include, path
from django.contrib import admin

from product import views as product_views
from users import views as users_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    #PRODUCT APP
    path('', product_views.index, name='index'),
    path('legals/', product_views.legals, name='legals'),
    path('products/', product_views.Product().results, name='products'),
    path('substitutes/', product_views.Product().substitutes, name='substitutes'),
    path('food/', product_views.Product().food, name='food'),
    path('change_favorite/', product_views.Product().change_favorite, name='change_favorite'),
    path('favorites/', product_views.Product().favorites, name='favorites'),
    
    #USERS APP
    path('register/', users_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name="logout"),
    path('profile/', users_views.profile, name='profile'),
]

"""if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns"""