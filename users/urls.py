from django.urls import path

from . import views # import views so we can use them in urls.

app_name='users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]