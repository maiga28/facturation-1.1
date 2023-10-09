from django.db import models
#from factures.models import Facture

class Payment(models.Model):
    factures = models.ForeignKey('factures.Facture', on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=100)

    def __str__(self):
        return f"Payment for Facture {self.factures.numero}"

    def save(self, *args, **kwargs):
        super(Payment, self).save(*args, **kwargs)