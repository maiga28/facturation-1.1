# Dans payment/admin.py
from django.contrib import admin
from .models import Payment

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('facture', 'date', 'amount', 'payment_method', 'payment_intent_id')

admin.site.register(Payment, PaymentAdmin)
