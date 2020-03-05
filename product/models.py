from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# from django.db import models

class Favorite(models.Model):

    code = models.CharField(max_length=30, primary_key=True ,unique=True)
    name = models.CharField(max_length=200)
    img = models.URLField(max_length=300)
    category = models.TextField()
    details = models.TextField()
    brand = models.CharField(max_length=200)
    brand_link = models.URLField(max_length=300)
    nutrigrade = models.CharField(max_length=2)
    nutriscore = models.IntegerField()
    stores = models.TextField()
    link = models.URLField(max_length=300)
    ingredients = models.TextField()
    fat_100g = models.FloatField()
    level_salt = models.CharField(max_length=30)
    saturated_fat_100g = models.FloatField()
    level_saturated_fat = models.CharField(max_length=30)
    salt_100g = models.FloatField()
    level_salt= models.CharField(max_length=30)
    sugar_100g = models.FloatField()
    level_sugar = models.CharField(max_length=30)
    nova = models.IntegerField()

    def __str__(self):
        return self.name

class Favorites(models.Model):

    saved_product = models.ForeignKey(Favorite, on_delete=models.CASCADE)
    saved_by = models.ForeignKey(User, on_delete=models.CASCADE)
