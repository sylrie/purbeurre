from django.test import TestCase, Client
from django.urls import resolve, reverse
from django.shortcuts import render

from product.views import index, legals, Product

class TestUrls(TestCase):

    def setUp(self):
        self.client = Client()

    def test_index_page_status_code(self):
        response = self.client.get("/")
        self.assertEquals(response.status_code, 200)

    def test_index_url_is_resolved(self):
        url = reverse("index")
        self.assertEquals(resolve(url).func, index)
    
    def test_legals_url_is_resolved(self):
        url = reverse("legals")
        self.assertEquals(resolve(url).func, legals)

    """def test_products_url_is_resolved(self):
        url = reverse("products")
        self.assertEqual(resolve(url).func, Product().results)
    
    def test_substitutes_url_is_resolved(self):
        url = reverse("substitutes")
        self.assertEqual(resolve(url).func, Product().substitutes)
    
    def test_food_url_is_resolved(self):
        url = reverse("food")
        self.assertEqual(resolve(url).func, Product().food)"""


