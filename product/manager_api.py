""" managerAPI
    manage the API request
"""

#! /usr/bin/env python3
# coding: UTF-8

from requests import get
import json
import pprint


class Product():
    def __init__(self):
        
        

        self.code = ""
        self.category = ""
        self.name = ""
        self.img = ""
        self.details = ""
        self.brand = ""
        self.brand_link = ""
        self.off_link = ""
        self.nutrigrade = "nc"
        self.stores = ""
        self.ingredients = ""
        self.nutriments = {
            "fat_100g": ("nc", "nc"),
            "saturated_fat_100g": ("nc", "nc"),
            "salt_100g": ("nc", "nc"),
            "sugar_100g": ("nc", "nc"),
            "nova": "",
        }
        
        
    
    def create_product(self, data):
        self.data = data
        try:
            self.code = self.data["code"]
            self.category = self.data["compared_to_category"]
            self.name = self.data["product_name"]
            self.img = self.data["image_url"]
            self.details = self.data["generic_name"]
            self.brand = self.data["brands"]
            self.brand_link = self.data["link"]
            self.off_link = self.data["url"]
            self.nutrigrade = self.data["nutrition_grades"]
            self.stores = self.data["stores"]
            self.ingredients = self.data["ingredients_text_fr"].replace("_", " ")
            self.nutriments["fat"] = (self.data["nutriments"]["fat_100g"], self.data["nutrient_levels"]["fat"])
            self.nutriments["saturated_fat"] = (self.data["nutriments"]["saturated-fat_100g"], self.data["nutrient_levels"]["saturated-fat"])
            self.nutriments["salt"] = (self.data["nutriments"]["fat_100g"], self.data["nutrient_levels"]["salt"])
            self.nutriments["sugar"] = (self.data["nutriments"]["sugars_100g"], self.data["nutrient_levels"]["sugars"])
            self.nutriments["nova"] = self.data["nutriments"]["nova-group"]

        except Exception as err:
            pass
        return self

class ManagerApi():
    
    def __init__(self):
        self.product_list = []

    def request_api(self, params):
        """ Make a API request for a selected category"""

        url = "https://world.openfoodfacts.org/cgi/search.pl"
        
        request = get(url=url, params=params)

        return request.json()

    def search_product(self, user_request):
        """ give a list of products matching with the use request""" 
        
        params = {
            'search_simple': 1,
            'action': 'process',
            'json': 1,
            'page_size': 12,
            'search_terms': "{}".format(user_request),
        }

        data = self.request_api(params)
      
        for product_data in data["products"]:
            
            product = Product(product_data)
            self.product_list.append(product)
            
        return self.product_list

    def search_substitutes(self, category, nutrigrade):
        """ give a list of substitutes in the relevant category """
        data = {}

        nutrigrades = [
            "a",
            "b",
            "c",
            "d",
            "e"
        ]

        for grade in nutrigrades:
            
            params = {
                'search_simple': 1,
                'action': 'process',
                'json': 1,
                'page_size': 10,
                'tagtype_0': 'categories',
                'tag_contains_0': 'contains',
                "tag_0": "{}".format(category),
                'tagtype_1': 'nutrition_grades',
                'tag_contains_1': 'contains',
                "tag_1": "{}".format(grade),
            }
            
            data = self.request_api(params)
            
            for product_data in data["products"]:
            
                product = Product().create_product(product_data)
                
                self.product_list.append(product)
                print(product.__dict__)
            if grade == nutrigrade:
                break
        #print(self.product_list[0].__dict__)
        return self.product_list

liste = ManagerApi().search_substitutes("fr:barres-chocolatees-au-lait", "e")
print(len(liste))
for food in liste:
    print(food.nutrigrade)