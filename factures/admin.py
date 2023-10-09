from django.contrib import admin
from .models import Facture

class FactureAdmin(admin.ModelAdmin):
    list_display = ['numero', 'client', 'remise', 'montant_total', 'statut', 'date_creation', 'date_mise_a_jour']

admin.site.register(Facture, FactureAdmin)
