from django.contrib import admin
from .models import Facture

class LigneFactureInline(admin.TabularInline):
    model = Facture.produits.through
    extra = 1

class FactureAdmin(admin.ModelAdmin):
    list_display = ['numero', 'date_emission', 'client', 'montant_total', 'statut']
    search_fields = ['numero', 'client__nom'] 
    list_filter = ['statut']
    inlines = [LigneFactureInline]

    actions = ['liquider_facture', 'annuler_facture']

    def liquider_facture(modeladmin, request, queryset):
        for facture in queryset:
            facture.liquider_facture()
            modeladmin.message_user(request, f"Les factures ont été liquides avec succès.")
            liquider_facture.short_description = "Liquider les factures sélectionnées"

    def annuler_facture(modeladmin, request, queryset):
        for facture in queryset:
            facture.annuler_facture()
            modeladmin.message_user(request, f"Les factures ont été annulées avec succès.")
            annuler_facture.short_description = "Annuler les factures sélectionnées"

admin.site.register(Facture, FactureAdmin)
