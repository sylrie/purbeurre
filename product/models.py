from django.db import models

# Create your models here.
# from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200, unique=True)
    category = models.CharField(max_length=200)
    brand = models.CharField(max_length=200)
    img = models.CharField(max_length=200, unique=True)
    details = models.CharField(max_length=500, unique=True)
    nutigrade = models.CharField(max_length=200)
    stores = models.CharField(max_length=200)
    link = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name