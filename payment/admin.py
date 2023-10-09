from django.contrib import admin
from .models import Payment

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('factures', 'date', 'amount', 'payment_method')  # Utilisez les noms corrects des champs du modèle Payment

admin.site.register(Payment, PaymentAdmin)
