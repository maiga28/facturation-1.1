# factures/models.py
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from decimal import Decimal
from django.db.models import Sum
from clients.models import Client
from products.models import Product

class Facture(models.Model):
    STATUT_CHOICES = [
        ('brouillon', 'Brouillon'),
        ('envoye', 'Envoyé'),
        ('paye', 'Payé'),
        ('annule', 'Annulé'),
    ]

    numero = models.AutoField(primary_key=True)
    date_emission = models.DateField(default=timezone.now)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='factures')
    remise = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='brouillon')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_mise_a_jour = models.DateTimeField(auto_now=True)

    # Spécifiez un related_name distinct pour éviter le conflit
    payments = models.ManyToManyField('payment.Payment', blank=True, related_name='facture_payments')

    produits = models.ManyToManyField(Product, through='LigneFacture', related_name='factures')

    def __str__(self):
        return str(self.numero)

    def calculer_total(self):
        total = Decimal(0)
        for ligne_facture in self.lignefacture_set.all():
            total += ligne_facture.sous_total
        return int(total)

    def save(self, *args, **kwargs):
        from payment.models import Payment
        self.montant_total = self.calculer_total() - self.remise
        super(Facture, self).save(*args, **kwargs)

    # ... (le reste du code reste inchangé)



    def liquider_facture(self):
        for ligne_facture in self.lignefacture_set.all():
            produit = ligne_facture.produit
            quantite_vendue = ligne_facture.quantite

            if quantite_vendue > produit.stock_quantity:
                raise Exception("Stock insuffisant pour le produit '{}'.".format(produit.title))

            produit.stock_quantity -= quantite_vendue
            produit.save()

    @classmethod
    def calculer_montant_total(cls, facture_id):
        facture = cls.objects.get(pk=facture_id)
        montant_total = facture.calculer_total() - facture.remise
        return montant_total

    @classmethod
    def est_facture_payee(cls, facture_id):
        facture = cls.objects.get(pk=facture_id)
        montant_total = facture.calculer_total() - facture.remise
        paiements_total = facture.payments.aggregate(Sum('amount'))['amount__sum'] or 0
        return montant_total <= paiements_total

    def annuler_facture(self):
        self.statut = 'annule'
        self.save()



class LigneFacture(models.Model):
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE)
    produit = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    sous_total = models.DecimalField(max_digits=10, decimal_places=2) 

    def save(self, *args, **kwargs):
        self.sous_total = self.prix_unitaire * self.quantite 
        super(LigneFacture, self).save(*args, **kwargs)
