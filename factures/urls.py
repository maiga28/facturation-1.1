from django.urls import path
from . import views

app_name = 'factures'  # Définissez le namespace pour l'application "factures"

urlpatterns = [
    path('creer_facture/', views.creer_facture, name='creer_facture'),
    path('liste_facture/', views.liste_factures, name='liste_factures'),
    path('facture/<int:pk>/', views.facture_detail, name='facture_detail'),
    #path('facture/<int:facture_id>/', views.facture_detail, name='facture_detail'),
]
