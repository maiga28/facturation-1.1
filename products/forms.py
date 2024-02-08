from django import forms
from .models import Product  # Assure-toi d'importer le modèle correctement

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product  # Utilise le modèle correct

        # Liste des champs que tu veux inclure dans le formulaire
        fields = ('title', 'category', 'description', 'price', 'stock_quantity')
