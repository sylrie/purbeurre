""" managerAPI
    manage the API request
"""

#! /usr/bin/env python3
# coding: UTF-8

from requests import get
import pprint

class ManagerApi():
    """ manage the API request """

    def __init__(self):

        self.food_data = {
            "code": "",
            "category": "",
            "name": "",
            "img": "",
            "details": "",
            "brand": "",
            "brand_link": "",
            "nutrigrade": "",
            "nutriscore": "",
            "stores": "",
            "link": "",
            "ingredients": "",
            "nutriments": "",
            }

        self.product_list = []

    def request_api(self, params):
        """ Make a API request for a selected category"""

        url = "https://world.openfoodfacts.org/cgi/search.pl"
        
        request = get(url=url, params=params)

        return request.json()

    def get_list(self, food_data, product):
        """ Add foods into product_list"""
        
        
        try:

            food_data["code"] = product["code"]
            food_data["category"] = product["compared_to_category"]
            food_data["name"] = product["product_name"]
            food_data["img"] = product["image_url"]
            food_data["details"] = product["generic_name_fr"]
            food_data["brand"] = product["brands"]
            food_data["brand_link"] = product["link"]
            food_data["nutrigrade"] = product["nutrition_grades"]
            food_data["nutriscore"] = int(product["nutriments"]["nutrition-score-fr"])
            food_data["stores"] = product["stores"]
            food_data["link"] = product["url"]
            food_data["ingredients"] = product["ingredients_text_fr"]
            food_data["fat_100g"] = float(product["nutriments"]["fat_100g"])
            food_data["saturated_fat_100g"] = float(product["nutriments"]["saturated-fat_100g"])
            food_data["salt_100g"] = float(product["nutriments"]["salt_100g"])
            food_data["sugar_100g"] = float(product["nutriments"]["sugars_100g"])
            food_data["nova"] = int(product["nutriments"]["nova-group_100g"])
            
            self.product_list.append(food_data)
        except Exception as error:
                pass

    
    def search_product(self, user_request):
    
        params = {
            'search_simple': 1,
            'action': 'process',
            'json': 1,
            'page_size': 5,
            'search_terms': "{}".format(user_request),
        }

        data = self.request_api(params)
        for product in data["products"]:

            self.food_data = self.get_list(product)
         
        
        return self.product_list

    def search_substitutes(self, category):
        

        params = {
            'search_simple': 1,
            'action': 'process',
            'json': 1,
            'page_size': 10,
            'tagtype_0': 'categories',
            'tag_contains_0': 'contains',
            "tag_0": "{}".format(category),
        }
        
        data = self.request_api(params)
       
        for product in data["products"]:
            food_data = self.food_data
            food = self.get_list(food_data, product)
            #print(food["name"])
            
            
          
        
            
        return self.product_list

food = ManagerApi()
food_list = food.search_substitutes("en:chocolate-nuts-cookie-bars")
print(type(food_list))
print(len(food_list))

for food in food_list:
   print(food["name"])
