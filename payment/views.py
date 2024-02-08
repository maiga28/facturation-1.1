from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.db.models import Sum
from .models import Payment
from .forms import PaymentForm
from factures.models import LigneFacture, Facture
from django.contrib.auth.decorators import login_required

from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Sum
from .models import Payment
from factures.models import Facture
from .forms import PaymentForm

@method_decorator(login_required, name='dispatch')
class AddPaymentView(View):
    template_name = 'payment/add_payment.html'

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        facture = get_object_or_404(Facture, pk=pk)
        payments = Payment.objects.filter(facture=facture)
        somme_total = payments.aggregate(Sum('amount'))['amount__sum'] or 0
        
        form = PaymentForm()
        context = {'form': form, 'somme_total': somme_total, 'facture': facture}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        facture = get_object_or_404(Facture, pk=pk)
        payments = Payment.objects.filter(facture=facture)
        somme_total = payments.aggregate(Sum('amount'))['amount__sum'] or 0

        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.facture = facture

            ligne_facture = facture.lignefacture_set.first()
            if ligne_facture:
                product_price = ligne_facture.produit.price
                payment.amount = product_price

            payment.save()
            return redirect('factures:facture_detail', pk=facture.pk)

        context = {'form': form, 'somme_total': somme_total, 'facture': facture}
        return render(request, self.template_name, context)



from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone  # Ajout de l'importation pour timezone
import stripe

from .models import Facture, Payment

stripe.api_key = settings.STRIPE_SECRET_KEY

def creer_session_paiement(request, facture_id):
    facture = Facture.objects.get(pk=facture_id)
    montant_total = facture.calculer_total() - facture.remise

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'Facture',
                },
                'unit_amount': int(montant_total * 100),  # Convertir en cents
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(),
        cancel_url=request.build_absolute_uri(),
    )

    # Enregistrez l'ID de l'intention de paiement dans le modèle Facture
    facture.payment_intent_id = session.payment_intent
    facture.save()

    return JsonResponse({'session_id': session.id})
