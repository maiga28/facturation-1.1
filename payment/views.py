from django.shortcuts import render, get_object_or_404, redirect
from .models import Payment
from .forms import PaymentForm
from factures.models import LigneFacture,Facture

from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Sum  # la fonction Sum pour effectuer des agrégations

def add_payment(request, pk):
    facture = get_object_or_404(Facture, pk=pk)
    payments = Payment.objects.filter(factures=facture)  # importé le modèle Payment

    # Calculez la somme totale des montants des paiements associés à la facture
    somme_total = payments.aggregate(Sum('amount'))['amount__sum'] or 0  # la valeur par défaut 0 si la somme est None

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.factures = facture  

            ligne_facture = LigneFacture.objects.filter(facture=facture).first()
            if ligne_facture:
                product_price = ligne_facture.produit.price
                payment.amount = product_price  #  le montant du paiement sur le prix du produit

            payment.save()
            return redirect('factures:facture_detail', pk=facture.pk)  
    else:
        form = PaymentForm()

    return render(request, 'payment/add_payment.html', {'form': form, 'somme_total': somme_total})
