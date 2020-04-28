""" managerAPI
    manage the API request
"""

#! /usr/bin/env python3
# coding: UTF-8

from django.core.management.base import BaseCommand, CommandError
#from product.manager_api import request_api
from product.update_data import UpdateData
from product.models import BaseProduct, UpdateReport
import time


class Command(BaseCommand):

    help = 'Import Openfoodfacts products'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        
        start_time = time.time()
        print("Cleanning Database")
 
        to_delete = BaseProduct.objects.filter(favorite=0)
        to_keep = BaseProduct.objects.all()
        to_keep = len(to_keep) - len(to_delete)
        
        print("{} products keeped, {} products deleted".format(to_keep,len(to_delete)))

        to_delete.delete()
        
        products = UpdateData()
        rejected_products = products.rejected
        added_products = products.added_products
        total_products = BaseProduct.objects.all()
        duration = time.time() - start_time
        print("--{} products added in {} seconds--".format(
            added_products,
            round(duration, 3)
        ))
        print("--- TOTAL PRODUCTS IN DATABASE: {} ---".format(len(total_products)))

        update = UpdateReport.objects.create(
            keeped=to_keep,
            rejected=rejected_products,
            added=added_products,
            total=len(total_products),
            duration=duration,
        )
        update.save()
