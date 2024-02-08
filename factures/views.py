# facturation/views.py
from django.shortcuts import render, redirect
from clients.models import Client  # Assurez-vous que le nom du modèle est correct ici
from django.contrib.auth.decorators import login_required
from .forms import FactureForm
from factures.models import Facture



from django.shortcuts import render,HttpResponse, redirect,get_object_or_404
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
                ligne_facture = LigneFacture(facture=factures, produit=produit, quantite=quantite, prix_unitaire=prix_unitaire, sous_total=sous_total)
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
@login_required
def liste_factures(request):
    factures = Facture.objects.all()  # Utilisez le nom de variable au pluriel pour la liste de factures
    return render(request, 'factures/liste_facture.html', {'factures': factures})  # Assurez-vous que le nom du dossier du template est correct

@login_required
def facture_detail(request, pk):
    facture = Facture.objects.get(pk=pk)
    lignes_facture = LigneFacture.objects.filter(facture=facture)
    total = facture.calculer_total()
    totals = int(total)
    total_produits = sum(ligne_facture.sous_total for ligne_facture in lignes_facture)
    prix_produits = [ligne_facture.produit.price for ligne_facture in lignes_facture]
    quantites = [ligne_facture.quantite for ligne_facture in lignes_facture]

    # Utilisez directement la relation 'payments' comme un attribut
    payments = facture.payments.all()

    statut_facture = facture.statut
    context = {
        'facture': facture,
        'total_produits': total_produits,
        'payments': payments,  # Utilisez directement la relation 'payments'
        'produits': Product.objects.all(),
        'prix_produits': prix_produits,
        'quantites': quantites,  # Utilisez 'quantites' plutôt que 'quantite'
        'statut_facture': statut_facture
    }

    return render(request, 'factures/facture_detail.html', context)


@login_required
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
