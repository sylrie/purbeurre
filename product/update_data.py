""" managerAPI
    manage the API request
"""

#! /usr/bin/env python3
# coding: UTF-8


from .manager_api import request_api
from .models import BaseProduct

class UpdateData():

    def __init__(self):
        self.products_list = []
        self.category_list = [
            "viandes",
            "snacks",
            "Aliments et boissons à base de végétaux",
            "Aliments à base de fruits et de légumes",
            "Produits laitiers",
            "Desserts"
            ]

        self.nutrigrades = [
            "a",
            "b",
            #"c",
            #"d",
            #"e"
        ]
        self.rejected = 0
        self.added_products = 0
        self.get_products()

    def get_products(self):
        """ give a list of substitutes in the relevant category """
        for category in self.category_list:
           
            if len(BaseProduct.objects.all()) < 8000:  
            
                self.products_list = []
                print("--CATEGORY: {}--".format((category.upper())))

                for grade in self.nutrigrades:

                    self.product_found = 0

                    print("Looking products with nutrigrade: {}...".format(grade))
                
                    params = {
                        "action": "process",
                        "tagtype_0": "categories",
                        "tag_contains_0": "contains",
                        "tag_0": "{}".format(category),
                        "tagtype_1": "nutrition_grades",
                        "tag_contains_1": "contains",
                        "tag_1": "{}".format(grade),
                        "page_size": 1000,
                        "json": "1",
                    }
                    try:
                        data = request_api(params)

                        for product in data["products"]:
                            
                            self.products_list.append(product)
                    except:
                        pass
                self.add_data(self.products_list)  
            else:
                print("! Limite de quantitée atteinte !")
                break

        return (self.added_products, self.rejected)
    
    def add_data(self, products_list):

        print(">> Adding products")
        missing_data = 0
        added = 0
        for product in products_list:   
            try:
                if not BaseProduct.objects.filter(code=product["code"]):
                    new = BaseProduct(
                        code = product["code"],
                        category = product["compared_to_category"],
                        name = product["product_name"],
                        img = product["image_url"],
                        details = product["generic_name_fr"],
                        brand = product["brands"],
                        stores = product["stores"],
                        nutrigrade = product["nutrition_grades"],
                        ingredients = product["ingredients_text_fr"].replace("_", " "),
                        fat = float(product["nutriments"]["fat_100g"]),
                        saturated_fat = float(product["nutriments"]["saturated-fat_100g"]),
                        salt = float(product["nutriments"]["salt_100g"]),
                        sugar = float(product["nutriments"]["sugars_100g"]),
                        level_fat = product["nutrient_levels"]["fat"],
                        level_saturated_fat = product["nutrient_levels"]["saturated-fat"],
                        level_salt = product["nutrient_levels"]["salt"],
                        level_sugar = product["nutrient_levels"]["sugars"],
                        nova = product["nutriments"]["nova-group"]
                    )
                    new.save()
                    added += 1
            except Exception :
                missing_data += 1

        self.rejected += missing_data
        self.added_products += added
        print("{} products added".format(added))  
        print("{} products rejected (missing_data)".format(missing_data))  
