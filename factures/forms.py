# facturation/forms.py
from django import forms
from .models import Facture,LigneFacture

# # facturation/forms.py
from django import forms

class LigneFactureForm(forms.ModelForm):
    class Meta:
        model = LigneFacture
        fields = ['quantite']

class FactureForm(forms.ModelForm):
    lignes_facture = forms.inlineformset_factory(Facture, LigneFacture, form=LigneFactureForm, extra=1)
    
    class Meta:
        model = Facture
        fields = ['client', 'produits','numero','remise','montant_total','statut']
