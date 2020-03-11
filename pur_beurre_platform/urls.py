from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.urls import include, path
from django.contrib import admin

from users import views as users_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('product.urls')),
    path('', include('users.urls')),
]
