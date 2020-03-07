from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# from django.db import models

class Favorite(models.Model):

    code = models.CharField(max_length=30, primary_key=True ,unique=True)
    name = models.CharField(max_length=200)
    img = models.URLField(max_length=300)
    details = models.TextField()
    nutrigrade = models.CharField(max_length=2)

    def __str__(self):
        return self.name

class Favorites(models.Model):

    saved_product = models.ForeignKey(Favorite, on_delete=models.CASCADE)
    saved_by = models.ForeignKey(User, on_delete=models.CASCADE)
