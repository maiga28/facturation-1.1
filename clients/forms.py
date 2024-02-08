from django import forms
from .models import Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'adresse', 'numero_telephone', 'adresse_email', 'ville', 'pays','apropos',
    ]