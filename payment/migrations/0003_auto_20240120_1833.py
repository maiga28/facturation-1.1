# Generated by Django 3.2.16 on 2024-01-20 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_rename_invoice_payment_factures'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='factures',
            new_name='facture',
        ),
        migrations.AddField(
            model_name='payment',
            name='payment_intent_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
