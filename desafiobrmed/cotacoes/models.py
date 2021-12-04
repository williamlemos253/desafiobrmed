from django.db import models

# Create your models here.

class Taxas(models.Model):
    date = models.DateField(unique_for_date=True)
    taxa_dolar = models.FloatField()
    taxa_real = models.FloatField()
    taxa_iene = models.FloatField()
    taxa_euro = models.FloatField()
