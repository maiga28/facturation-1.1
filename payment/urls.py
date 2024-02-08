# facturation/urls.py
from django.urls import path
from .views import AddPaymentView

from . import views
app_name = 'payment'
urlpatterns = [
   
     path('make_payment/<int:pk>/', AddPaymentView.as_view(), name='make_payment'),
   # path('payment_detail/<int:invoice_id>/', views.payment_detail, name='payment_detail'),
   
]
