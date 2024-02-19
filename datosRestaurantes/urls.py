from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.hogar), #inicio
    path('datos/', views.restaurantes_path), #todos los restaurantes
    path('datos/<uuid:pk>/', views.restaurante_path) #Restaurantes por id
]
