from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'stock_quantity', 'date_added')  # Champs à afficher dans la liste

admin.site.register(Product, ProductAdmin)
