""" managerAPI
    manage the API request
"""

#! /usr/bin/env python3
# coding: UTF-8

from requests import get
import pprint

def request_api(params):
    """ Make a API request for a selected category"""

    url = "https://world.openfoodfacts.org/cgi/search.pl"
    
    request = get(url=url, params=params)

    return request.json()
    
def get_data_list(data):
    """ Add foods into product_list"""
    product_list = []
    
    for product in data["products"]:
        food_data = {
            }
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
            food_data["fat_100g"] = float(product["nutriments"]["fat_100g"])
            food_data["saturated_fat_100g"] = float(product["nutriments"]["saturated-fat_100g"])
            food_data["salt_100g"] = float(product["nutriments"]["salt_100g"])
            food_data["sugar_100g"] = float(product["nutriments"]["sugars_100g"])
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
    """ Add foods into product_list"""
    food_data = {
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
        "fat_100g": "",
        "saturated_fat_100g": "",
        "salt_100g": "",
        "sugar_100g": "",
        "level_fat": "",
        "level_saturated_fat": "",
        "level_salt": "",
        "level_sugar": "",
        "nova": "",
    }   
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
        #food_data["link"] = product["url"]
        food_data["ingredients"] = product["ingredients_text_fr"].replace("_", " ")
        food_data["fat_100g"] = float(product["nutriments"]["fat_100g"])
        food_data["saturated_fat_100g"] = float(product["nutriments"]["saturated-fat_100g"])
        food_data["salt_100g"] = float(product["nutriments"]["salt_100g"])
        food_data["sugar_100g"] = float(product["nutriments"]["sugars_100g"])
        food_data["level_fat"] = product["nutrient_levels"]["fat"]
        food_data["level_saturated_fat"] = product["nutrient_levels"]["saturated-fat"]
        food_data["level_salt"] = product["nutrient_levels"]["salt"]
        food_data["level_sugar"] = product["nutrient_levels"]["sugars"]
        food_data["nova"] = product["nutriments"]["nova-group"]
       

    except Exception:
            pass
        
    return food_data

def search_product(user_request):
    """ give a list of products matching with the use request""" 
    
    params = {
        'search_simple': 1,
        'action': 'process',
        'json': 1,
        'page_size': 30,
        'search_terms': "{}".format(user_request),
    }

    data = request_api(params)
    product_list = get_data_list(data)
    
    return product_list

def search_substitutes(category, nutrigrade):
    """ give a list of substitutes in the relevant category """
    product_list = []
    data = {}
    quality ="better"
    nutrigrades = [
        "a",
        "b",
        "c",
        "d",
        "e"
    ]

    for grade in nutrigrades:
        if grade == nutrigrade:
            if len(product_list) > 0:
                break
            else:
                quality = "equal"

        params = {
            'search_simple': 1,
            'action': 'process',
            'json': 1,
            'page_size': 50,
            'tagtype_0': 'categories',
            'tag_contains_0': 'contains',
            "tag_0": "{}".format(category),
            'tagtype_1': 'nutrition_grades',
            'tag_contains_1': 'contains',
            "tag_1": "{}".format(grade),
        }
        
        data_grade = request_api(params)
        
        data = get_data_list(data_grade)

        product_list.extend(data)
        
        if len(product_list) > 30:
            break
        

    return (product_list, quality)
    
def select_product(code):
    """ give all data for a selected product """

    url = "https://world.openfoodfacts.org/api/v0/produit/"+str(code)+".json"
    
    product = get(url).json()

    food_data = get_product_list(product["product"])

    return food_data
