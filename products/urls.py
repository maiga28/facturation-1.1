from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('products/', views.liste_products, name='liste_products'),
    path('nouveau_produit/', views.nouveau_produit, name='nouveau_produit'),
    path('products/modifier/<int:pk>/', views.modifier_products, name='modifier_products'),
    path('products/supprimer/<int:pk>/', views.supprimer_products, name='supprimer_products'),
]
