from django.db import models
from clients.models import Client
from products.models import Product
from payment.models import Payment
from django.utils import timezone
from decimal import Decimal

class Facture(models.Model):
    STATUT_CHOICES = [
        ('brouillon', 'Brouillon'),
        ('envoye', 'Envoyé'),
        ('paye', 'Payé'),
        ('annule', 'Annulé'),
    ]
    payments = models.ManyToManyField(Payment, blank=True)
    numero = models.AutoField(primary_key=True)
    date_emission = models.DateField(default=timezone.now)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    produits = models.ManyToManyField(Product, through='LigneFacture')
    remise = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='brouillon')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_mise_a_jour = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.numero)
    
    def calculer_total(self):
        total = Decimal(0)
        for ligne_facture in self.lignefacture_set.all():
            total += ligne_facture.sous_total
        return total

    def save(self, *args, **kwargs):
        self.montant_total = self.calculer_total() - self.remise
        super(Facture, self).save(*args, **kwargs)

class LigneFacture(models.Model):
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE)
    produit = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    sous_total = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.sous_total = self.prix_unitaire * self.quantite
        super(LigneFacture, self).save(*args, **kwargs)
