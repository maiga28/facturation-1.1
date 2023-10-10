from sqlite3 import IntegrityError
# from django.shortcuts import render

# # Create your views here.
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import ProductForm



def liste_products(request):
    products = Product.objects.order_by('title')
    context = {'products': products}
    search_query = request.GET.get('title')
    if search_query and search_query != '':
        products = Product.objects.filter(title__icontains=search_query)
    else:
        products = Product.objects.all()
    context = {
        'products': products,  
        'search_query': search_query
    }
    return render(request, 'products/liste_products.html', context)
# #######################################################################################################

# #######################################################################################################

from django.utils.text import slugify
from django.db import IntegrityError

from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.utils.text import slugify
from .models import Product
from .forms import ProductForm  # Assure-toi d'importer ton formulaire

# def nouveau_produit(request):
#     produits = Product.objects.all()
# #    paginator = Paginator(produits, 8)

#    # page_number = request.GET.get('page')  # Obtient le numéro de page à partir des paramètres GET
#    # page_obj = paginator.get_page(page_number)  # Obtient l'objet Page correspondant au numéro de page
    
#     if request.method == 'POST':
#         form = ProductForm(request.POST, request.FILES)
        
#        # return HttpResponse(produits)
#         if request.method == 'POST':
#             form = ProductForm(request.POST)
#         if form.is_valid():
#             form.save() # Générer le slug à partir du nom du produit
#             # Vérifier si un produit avec le même slug existe déjà
#             counter = 1
#             while Product.objects.filter(slug=slug).exists():
#                 counter += 1
#                 slug = f"{slug}-{counter}"
            
#             # Créer une instance de Produit
#            # produit = Product(title=title, prix=price, stock_quantity=stock_quantity, image=image, description=description, slug=slug)
#             try:
#                 form.save()
               
#             except IntegrityError:
#                 # Gérer les erreurs de sauvegarde dues à un conflit de clé unique
#                 message = "Un produit avec le même nom existe déjà."
#                 context = {'form': form, 'message': message}
#                 return render(request, 'products/add_products.html', context)
#             return redirect('produits:nouveau_produit')
#     else:
#         form = ProductForm()
#     produits = Product.objects.all()  # Récupérer tous les produits
#     context = {
#         'form': form,
#         'produits': produits,
#      #   'produits': page_obj,
#         'produit': produits,
#     }
#     return render(request, 'products/add_products.html', context)

def modifier_products(request, pk):
    product = get_object_or_404(Product, pk=pk)
     # Reste du code...

    if request.method == 'POST':
         form = ProductForm(request.POST, instance=product)
         if form.is_valid():
             form.save()
             return redirect('products:liste_products')
    else:
         form = ProductForm(instance=product)
    return render(request, 'products/modifier_products.html', {'form': form, 'product': product})

def supprimer_products(request, pk):
     # Votre code ici

    products = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
         products.delete()
         return redirect('products:liste_products')
    return render(request, 'products/supprimer_products.html', {'products': products})


from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import ProductForm

@login_required
def nouveau_produit(request):
   
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            #user = User
            product = form.save(commit=False)  # N'enregistre pas encore le produit dans la base de données
        product.user = request.user  # Associe l'utilisateur actuel au produit
        product.save()
        return redirect('products:liste_products')
    else:
        form = ProductForm()
    
    return render(request, 'products/add_products.html', {'form': form})


    