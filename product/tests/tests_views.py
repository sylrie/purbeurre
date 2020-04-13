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
        self.assertTemplateUsed(response, 'product/home.html')

    def test_legals(self): 
        response = self.client.get(reverse('legals'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/legals.html')

    def test_results(self):
        response = self.client.post(reverse('products'), {'product-name': 'Confipote Fraise'})
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/product.html')
        self.assertContains(response, 'Confipote')

    def test_food(self):
        response = self.client.get(reverse('food'), {'code': '3021762383306'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/food.html')
        self.assertContains(response, 'Confipote Fraise')

    def test_substitutes(self):
        response = self.client.get(reverse('substitutes'), {'code': '3021762383306'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/product.html')
        self.assertContains(response, 'Confiture')
   
    """def test_favorites(self):
        response = self.client.get(reverse('favorites'), {'title': 'Pur Beurre - Favoris'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/favorites.html')
        self.assertContains(response, 'Pur Beurre - Favoris')"""