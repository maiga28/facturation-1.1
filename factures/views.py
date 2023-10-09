# facturation/views.py
from django.shortcuts import render, redirect
from clients.models import Client  # Assurez-vous que le nom du modèle est correct ici
from django.contrib.auth.decorators import login_required
from .forms import FactureForm




from django.shortcuts import render, redirect,get_object_or_404
from .forms import FactureForm  # Assurez-vous d'importer votre formulaire FactureForm
from .models import Facture, LigneFacture
from products.models import Product
from django.http import HttpResponse




@login_required
def creer_facture(request):
    if request.method == 'POST':
        form = FactureForm(request.POST)
        if form.is_valid():
            factures = form.save(commit=False)
            factures.save()

            for produit in form.cleaned_data['produits']:
                quantite = request.POST.get(f'quantite_produit_{produit.id}')  # Obtenir la quantité du produit par son ID
                quantite = int(quantite) if quantite else 0  # Assurez-vous que la quantité est un entier, par défaut à 0 si elle est vide

                prix_unitaire = produit.price
                sous_total = quantite * prix_unitaire
                ligne_facture = LigneFacture(factures=factures, produit=produit, quantite=quantite, prix_unitaire=prix_unitaire, sous_total=sous_total)
                ligne_facture.save()

            return redirect('factures:liste_factures')
    else:
        form = FactureForm()
        
    clients = Client.objects.all()
    produits = Product.objects.all()
    factures = Facture.objects.all()

    context = {
        'clients': clients,
        'produits': produits,
        'factures': factures,
        'form': form,
    }

    return render(request, 'factures/creer_facture.html', context)




from django.shortcuts import render
from .models import Facture  # Assurez-vous d'importer correctement le modèle Facture

def liste_factures(request):
    factures = Facture.objects.all()  # Utilisez le nom de variable au pluriel pour la liste de factures
    return render(request, 'factures/liste_facture.html', {'factures': factures})  # Assurez-vous que le nom du dossier du template est correct

def facture_detail(request, pk):
    factures = Facture.objects.get(pk=pk)  # Utilisez Facture.objects.get(pk=...) pour obtenir la factures
    total = factures.calculer_total()  
    payments = factures.payments.all()  # Récupérer les paiements associés à cette factures
    context = {
        'factures':factures,
        'total':total,
        'payments':payments
    }
    return render(request, 'factures/facture_detail.html', context)

def modifier_facture(request, pk):
    factures = get_object_or_404(Facture, pk=pk)
    if request.method == 'POST':
        form = FactureForm(request.POST, isinstance=factures)
        if form.is_valid():
            form.save()
            return redirect('factures:liste_factures')
        else:
            form = FactureForm(instance=factures)
        return render(request, 'factures/liste_facture.html', {'factures': factures})  
