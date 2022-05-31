from unicodedata import name
from django.urls import path
from . import views
    
urlpatterns = [
    path('', views.index, name = 'index'),
    path('login_register', views.login_register, name = 'login_register'),
    path('logout', views.logout, name = 'logout')
]