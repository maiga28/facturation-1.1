from django.db import models

# Create your models here.

class Client(models.Model):
    name = models.CharField(max_length=100)
    adresse = models.CharField(max_length=45)
    numero_telephone = models.IntegerField()
    adresse_email = models.EmailField()
    ville = models.CharField(max_length=50)
    pays = models.CharField(max_length=50)
    apropos = models.TextField()

    def __str__(self):
        return self.name
    
