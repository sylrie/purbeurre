from django.db import models

# Create your models here.
# from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200, primary_key=True ,unique=True)
    category = models.TextField()
    brand = models.CharField(max_length=200)
    brand_link = models.URLField(max_length=300)
    img = models.URLField(max_length=300)
    details = models.TextField()
    nutigrade = models.CharField(max_length=2)
    nutriscore = models.IntegerField()
    stores = models.TextField()
    link = models.URLField(max_length=300)
    ingredients = models.TextField()
    fat_100g = models.FloatField()
    saturated_fat_100g = models.FloatField()
    salt_100g = models.FloatField()
    sugar_100g = models.FloatField()
    nova = models.IntegerField()
    
    class Meta:
        verbose_name = "product"
        ordering = ['name']
        
    def __str__(self):
        return self.name