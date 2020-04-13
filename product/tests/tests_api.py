from django.test import TestCase, Client

from product.manager_api import ProductData

"""class TestApi(TestCase):

    def setUp(self):
        self.client = Client()
        
    def test_search_product(self):
        product = ProductData().search_product("user_request")
        self.assertIs(type(product), list)
    
    def test_search_substitutes(self):
        substitutes = ProductData().search_substitutes("category", "nutrigrade")
        self.assertIs(type(substitutes[0]), list)
        self.assertIs(type(substitutes[1]), str)
    
    def test_select_product(self):
        product = ProductData().select_product("code")
        self.assertIs(type(product), dict)"""