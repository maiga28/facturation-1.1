from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from django.shortcuts import render, redirect, get_object_or_404
from .models import Client
from .forms import ClientForm


def liste_clients(request):
    clients = Client.objects.order_by('name')
    context = {'clients': clients}
    search_query = request.GET.get('name')
    if search_query and search_query != '':
        clients = Client.objects.filter(name__icontains=search_query)
    else:
        clients = Client.objects.all()
    context = {
        'clients': clients,  # Utiliser 'clients' au lieu de 'client'
        'search_query': search_query
    }
    return render(request, 'clients/liste_clients.html', context)



def ajouter_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clients:liste_clients')
    else:
        form = ClientForm()
    return render(request, 'clients/ajouter_client.html', {'form': form})

def modifier_client(request, pk):
    client = get_object_or_404(Client, pk=pk)
    # Reste du code...

    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('clients:liste_clients')
    else:
        form = ClientForm(instance=client)
    return render(request, 'clients/modifier_client.html', {'form': form, 'client': client})

def supprimer_client(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        client.delete()
        return redirect('clients:liste_clients')
    return render(request, 'clients/supprimer_clients.html', {'client': client})

