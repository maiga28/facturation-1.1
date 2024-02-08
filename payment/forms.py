from django import forms
from .models import Payment
from datetime import timezone

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['date', 'amount', 'payment_method']

        labels = {
            'date': 'Date de paiement',
            'amount': 'Montant',
            'payment_method': 'Mode de paiement',
        }

        widgets = {
            'date': forms.DateInput(attrs={'class': 'datepicker', 'readonly': 'readonly'}),
            'amount': forms.TextInput(attrs={'class': 'custom-input'}),
            'payment_method': forms.Select(attrs={'class': 'custom-select'}),
        }

    def __init__(self, *args, **kwargs):
        facture = kwargs.pop('facture', None)
        super(PaymentForm, self).__init__(*args, **kwargs)
        
        if facture:
            self.fields['amount'].initial = facture.calculer_total() - facture.remise
            self.fields['date'].initial = timezone.now().date()
