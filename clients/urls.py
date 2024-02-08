from django.urls import path

from . import views

app_name = 'clients'

urlpatterns = [
    path('', views.liste_clients, name='liste_clients'),
    path('ajouter/', views.ajouter_client, name='ajouter_client'),
    #path('search/', views.search_clients, name='search_clients'),
    path('modifier/<int:pk>/', views.modifier_client, name='modifier_client'),
    path('supprimer/<int:pk>/', views.supprimer_client, name='supprimer_client'),
]
