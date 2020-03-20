""" Tables for products app """

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class BaseProduct(models.Model):

    code = models.CharField(max_length=30, primary_key=True, unique=True)
    category = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    img = models.URLField(max_length=300)
    details = models.TextField()
    brand = models.CharField(max_length=100)
    stores = models.CharField(max_length=200)
    nutrigrade = models.CharField(max_length=2)
    ingredients = models.TextField()
    fat = models.FloatField()
    saturated_fat = models.FloatField()
    salt = models.FloatField()
    sugar = models.FloatField()
    level_fat = models.CharField(max_length=50)
    level_saturated_fat = models.CharField(max_length=50)
    level_salt = models.CharField(max_length=50)
    level_sugar = models.CharField(max_length=50)
    nova = models.CharField(max_length=2)
    favorite = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class UpdateReport(models.Model):

    keeped = models.IntegerField()
    rejected = models.IntegerField()
    added = models.IntegerField()
    total = models.IntegerField()
    duration = models.FloatField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.date)

class FavoriteProduct(models.Model):
    """ Favorites table """

    saved_product = models.ForeignKey(BaseProduct, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(verbose_name="Date sauvegarde", default=timezone.now)

    def __str__(self):

        return str(self.saved_product)+" - ajouté par: "+str(self.user).capitalize()
