# forms.py

from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['date', 'amount', 'payment_method']

    # Ajoutez des classes CSS aux champs
    widgets = {
        'date': forms.DateInput(attrs={'class': 'datepicker'}),
        'amount': forms.TextInput(attrs={'class': 'custom-input'}),
        'payment_method': forms.Select(attrs={'class': 'custom-select'}),
    }
    labels = {
        'date': 'Date de paiement',
        'amount': 'Montant',
        'payment_method': 'Mode de paiement',
    }
