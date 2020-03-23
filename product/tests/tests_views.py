from django.test import TestCase, Client
from django.urls import resolve, reverse


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.product = {
            "code": "3021762383306",
            "name": "Confipote Fraise",
        }
        self.product_list = [
            {"name": "Fraise à tartiner sans sucres ajoutés"},
            {"name": "Confiture de Fraises au Maltitol"}
        ]
   
    def test_homepage(self): 
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Du gras")

    def test_legals(self): 
        response = self.client.get(reverse('legals'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "légales")

    def test_substitutes(self):
        response = self.client.get(reverse('substitutes'), {'code': '3021762383306'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Confiture')
    
        