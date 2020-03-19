""" managerAPI
    manage the API request
"""

#! /usr/bin/env python3
# coding: UTF-8

from requests import get

def request_api(params):
    """ Make a API request for a selected category"""

    url = "https://fr.openfoodfacts.org/cgi/search.pl"
    request = get(url=url, params=params)

    return request.json()

def get_data_list(data):
    """ Add foods into product_list"""
    product_list = []

    for product in data["products"]:
        food_data = {}
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
            food_data["ingredients"] = product["ingredients_text_fr"].replace("_", " ")
            food_data["fat"] = float(product["nutriments"]["fat_100g"])
            food_data["saturated_fat"] = float(product["nutriments"]["saturated-fat_100g"])
            food_data["salt"] = float(product["nutriments"]["salt_100g"])
            food_data["sugar"] = float(product["nutriments"]["sugars_100g"])
            food_data["level_fat"] = product["nutrient_levels"]["fat"]
            food_data["level_saturated_fat"] = product["nutrient_levels"]["saturated-fat"]
            food_data["level_salt"] = product["nutrient_levels"]["salt"]
            food_data["level_sugar"] = product["nutrient_levels"]["sugars"]
            food_data["nova"] = product["nutriments"]["nova-group_100g"]

            product_list.append(food_data)

        except:
            pass

    return product_list

def get_product_list(product):
    """ Add data into food_data"""
    food_data = {}
    try:
        food_data["code"] = product["code"]
        food_data["category"] = product["compared_to_category"]
        food_data["name"] = product["product_name"]
        food_data["img"] = product["image_url"]
        food_data["details"] = product["generic_name_fr"]
        food_data["brand"] = product["brands"]
        food_data["brand_link"] = product["link"]
        food_data["nutrigrade"] = product["nutrition_grades"]
        food_data["stores"] = product["stores"]
        food_data["ingredients"] = product["ingredients_text_fr"].replace("_", " ")
        food_data["fat"] = float(product["nutriments"]["fat_100g"])
        food_data["saturated_fat"] = float(product["nutriments"]["saturated-fat_100g"])
        food_data["salt"] = float(product["nutriments"]["salt_100g"])
        food_data["sugar"] = float(product["nutriments"]["sugars_100g"])
        food_data["level_fat"] = product["nutrient_levels"]["fat"]
        food_data["level_saturated_fat"] = product["nutrient_levels"]["saturated-fat"]
        food_data["level_salt"] = product["nutrient_levels"]["salt"]
        food_data["level_sugar"] = product["nutrient_levels"]["sugars"]
        food_data["nova"] = product["nutriments"]["nova-group"]

    except Exception:
        pass

    return food_data

class ProductData():

    def __init__(self):

        self.product = {}
        self.product_list = []
        self.substitutes_list = []

    def search_product(self, user_request):
        """ give a list of products matching with the use request"""

        params = {
            'search_simple': 1,
            'action': 'process',
            'json': 1,
            'page_size': 40,
            'search_terms': "{}".format(user_request),
        }

        data = request_api(params)
        self.products_list = get_data_list(data)

        return self.products_list

    def search_substitutes(self,category, nutrigrade):
        """ give a list of substitutes in the relevant category """

        self.substitutes_list = []
        data = {}
        self.quality = "better"
        nutrigrades = [
            "a",
            "b",
            "c",
            "d",
            "e"
        ]

        for grade in nutrigrades:
            if grade == nutrigrade:
                if len(self.substitutes_list) > 0:
                    break

                self.quality = "equal"

            params = {
                'search_simple': 1,
                'action': 'process',
                'json': 1,
                'page_size': 40,
                'tagtype_0': 'categories',
                'tag_contains_0': 'contains',
                "tag_0": "{}".format(category),
                'tagtype_1': 'nutrition_grades',
                'tag_contains_1': 'contains',
                "tag_1": "{}".format(grade),
            }

            data_grade = request_api(params)

            data = get_data_list(data_grade)

            self.substitutes_list.extend(data)

            if len(self.substitutes_list) > 0:
                break

        return (self.substitutes_list, self.quality)

    def select_product(self, code):
        """ give all data for a selected product """

        url = "https://world.openfoodfacts.org/api/v0/produit/"+str(code)+".json"

        product = get(url).json()

        self.food_data = get_product_list(product["product"])

        return self.food_data



