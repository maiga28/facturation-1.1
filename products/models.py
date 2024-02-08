from django.db import models
from django.utils.text import slugify
from autoslug import AutoSlugField
from django.core.validators import MinValueValidator
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

from django.db import models
from django.core.validators import MinValueValidator
from autoslug import AutoSlugField
from ckeditor.fields import RichTextField  # Si vous utilisez le plugin CKEditor

class Product(models.Model):
    title = models.CharField(max_length=30)
    category = models.CharField(max_length=30)
    description = RichTextField()
    slug = AutoSlugField(max_length=30, unique=True, populate_from='title')
    image = models.ImageField(upload_to='apps/static/assets/img')
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    stock_quantity = models.PositiveIntegerField(
        help_text="La quantité en stock",
        validators=[MinValueValidator(0)]
    )
    date_added = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date_added']
        verbose_name = "produit"
        verbose_name_plural = "produits"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def decrease_stock(self, quantity):
        self.stock_quantity -= quantity
        self.save()
