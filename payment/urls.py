# facturation/urls.py
from django.urls import path

from . import views
app_name = 'payment'
urlpatterns = [
    path('payment/<int:pk>/', views.add_payment, name='add_payment'),
   # path('payment_detail/<int:invoice_id>/', views.payment_detail, name='payment_detail'),
   
]
