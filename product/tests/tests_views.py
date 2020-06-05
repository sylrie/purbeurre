from django.test import TestCase, Client
from django.urls import resolve, reverse
from django.db.models.query import QuerySet
from django.contrib.auth.models import User

from product.models import FavoriteProduct, BaseProduct

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

        self.assertIs(type(response.context['products']), QuerySet)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/product.html')
        self.assertContains(response, 'Confipote')

    def test_food(self):
        response = self.client.get(reverse('food'), {'code': '3021762383306'})
   
        self.assertIs(type(response.context['food']), dict)
        self.assertIs(type(response.context['favorite']), bool)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/food.html')
        self.assertContains(response, 'Confipote')

    def test_substitutes(self):
        response = self.client.get(reverse('substitutes'), {'code': '3021762383306'})

        self.assertIs(type(response.context['products']), list)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/product.html')
        self.assertContains(response, 'Confiture')

    def test_top_6(self):
        response = self.client.get(reverse('top_6'))
        
        self.assertIs(type(response.context['products']), QuerySet)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Top 6 des utilisateurs')
        self.assertTemplateUsed(response, 'product/favorites.html')


    def test_flow_change_favorite(self):
        product = BaseProduct.objects.create(
            code='0001',
            category='category',
            name='productName',
            img='',
            details='blabla',
            brand='brand',
            stores='stores',
            nutrigrade='a',
            ingredients='ingredients',
            fat='1.1',
            saturated_fat='1.2',
            salt='1.3',
            sugar ='1.4',
            level_fat ='1.5',
            level_saturated_fat ='1.6',
            level_salt = '1.7',
            level_sugar ='1.8',
            nova ='1',
        )
        product.save()

        user = User.objects.create_user(
            username='toto',
            email='toto@toto.fr',
            password='password',
        )
        self.client.force_login(user)

        response = self.client.get(reverse('favorites'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/favorites.html')

        response = self.client.get(
            'http://127.0.0.1:8000/favorites/change/?add={}'.format(
                product.code
            )
        )
            
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/favorites.html')
        self.assertContains(response, 'Le produit à été ajouté aux favoris !')

        response = self.client.get(
            'http://127.0.0.1:8000/favorites/change/?del={}'.format(
                product.code
            )
        )
            
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/favorites.html')
        self.assertContains(response, 'Le produit à été retiré des favoris')

    def test_change_favorite_no_user(self):
        response = self.client.get(
            'http://127.0.0.1:8000/favorites/change/?add=0001'
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
