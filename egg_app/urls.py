
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add_data/', views.add_data, name='add_data'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('documentation/', views.documentation, name='documentation'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),


]
