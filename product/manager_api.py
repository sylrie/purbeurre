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

        self.categories = (
            #"Saucisson",
            #"Pizza",
            #"Chips",
            #"Yaourts",
            "Biscuits",
            "desserts"
            )

        self.food_list = []

        self.add_data()

    def request_api(self, category_name):
        """ Make a API request for a selected category"""

        url = "https://fr.openfoodfacts.org/cgi/search.pl"
        params = {
            'search_simple': 1,
            'action': 'process',
            'json': 1,
            'page_size': 5,
            'tagtype_0': 'categories',
            'tag_contains_0': 'contains',
            "tag_0": "{}".format(category_name),
            }

        request = get(url=url, params=params)

        return request.json()

    def add_data(self):
        """ Add foods into food_list"""

        for category in self.categories:

            data = self.request_api(category_name=category)

            for product in data["products"]:

                food_data = {
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

                try:

                    food_data["category"] = category
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

                    self.food_list.append(food_data)
                    
                except Exception as err:
                    print(err)
        return self.food_list
