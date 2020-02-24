import os
import requests
import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "pur_beurre_platform.settings"
)
django.setup()

from product.models import Product
from product.manager_api import ManagerApi


food_list = ManagerApi().food_list

Product.objects.all().delete()

for food in food_list:

    product = Product(
        name=food['name'],
        category=food['category'],
        brand=food['brand'],
        brand_link=food['brand_link'],
        img=food['img'],
        details=food['details'],
        nutigrade=food['nutrigrade'],
        nutriscore=food['nutriscore'],
        stores=food['stores'],
        link=food['link'],
        ingredients=food['ingredients'],
        fat_100g=food['fat_100g'],
        saturated_fat_100g=food['saturated_fat_100g'],
        salt_100g=food['salt_100g'],
        sugar_100g=food['sugar_100g'],
        nova=food['nova'],
    )
    product.save()