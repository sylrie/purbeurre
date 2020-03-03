from django.urls import path

from . import views # import views so we can use them in urls.

app_name='users'

urlpatterns = [
    path('create/', views.create_acount, name='create'),
    path('login/', views.login, name='login'),
]