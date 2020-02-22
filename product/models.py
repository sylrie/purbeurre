from django.db import models

# Create your models here.
# from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.TextField()
    brand = models.CharField(max_length=200)
    img = models.URLField(max_length=300)
    details = models.TextField()
    nutigrade = models.CharField(max_length=200)
    nutriscore = models.IntegerField()
    stores = models.TextField()
    link = models.URLField(max_length=300)
    ingredients = models.TextField()
    nutriments = models.TextField()

    def __str__(self):
        return self.name