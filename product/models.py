from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
# from django.db import models

class SavedProduct(models.Model):

    code = models.CharField(max_length=30, primary_key=True ,unique=True)
    name = models.CharField(max_length=200)
    img = models.URLField(max_length=300)
    details = models.TextField()
    nutrigrade = models.CharField(max_length=2)

    def __str__(self):
        return self.name

class FavoriteProduct(models.Model):

    saved_product = models.ForeignKey(SavedProduct, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(verbose_name="Date sauvegarde", default=timezone.now)

    def __str__(self):
       
        return str(self.saved_product)+" - ajouté par: "+str(self.user).capitalize()