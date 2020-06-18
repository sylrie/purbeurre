from django.test import TestCase, Client
from django.urls import resolve, reverse
from django.db.models.query import QuerySet
from django.contrib.auth.models import User
from unittest.mock import patch

from product.models import FavoriteProduct, BaseProduct, BaseProductManager

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        
        self.product = BaseProduct.objects.create(
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

        self.user = User.objects.create_user(
            username='toto',
            email='toto@toto.fr',
            password='password',
        )

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

    """def test_top_6(self):
        response = self.client.get(reverse('top_6'))
        
        self.assertIs(type(response.context['products']), QuerySet)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Top 6 des utilisateurs')
        self.assertTemplateUsed(response, 'product/favorites.html')"""

    def test_flow_change_favorite(self):

        self.product.save()

        self.client.force_login(self.user)

        response = self.client.get(reverse('favorites'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/favorites.html')

        # Save favorite
        response = self.client.get(
            '/favorites/change/?add={}'.format(
                self.product.code
            )
        )
            
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/favorites.html')
        self.assertContains(response, 'Le produit à été ajouté aux favoris !')

        # Delete favorite
        response = self.client.get(
            '/favorites/change/?del={}'.format(
                self.product.code
            )
        )
            
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/favorites.html')
        self.assertContains(response, 'Le produit à été retiré des favoris')

    def test_change_favorite_no_user(self):
        response = self.client.get(
            '/favorites/change/?add=0001'
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    @patch('product.models.BaseProductManager.get_top_6')
    def test_top_no_user(self, mock_get_top_6):
        mock_get_top_6.return_value = [
            BaseProduct(code='000'),
            BaseProduct(code='001'),
            BaseProduct(code='002'),
            BaseProduct(code='003'),
            BaseProduct(code='004'),
            BaseProduct(code='005'),
            BaseProduct(code='006'),
            BaseProduct(code='007'),
            ]
            
        response = self.client.get(reverse('top_6'))
        #import pdb
        #pdb.set_trace()
        self.assertContains(response, 'Connecte toi pour voir tes favoris')
        self.assertContains(response, 'Top 6 des utilisateurs')
        self.assertContains(response, '?code=005')
        self.assertNotContains(response, '?code=006')
        self.assertIs(type(response.context['products']), list)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/favorites.html')
       
    @patch('product.models.BaseProductManager.get_top_6')
    def test_top_user(self, mock_get_top_6):
        self.client.force_login(self.user)
        
        mock_get_top_6.return_value = [
            BaseProduct(code='000'),
            BaseProduct(code='001'),
            BaseProduct(code='002'),
            ]
            
        response = self.client.get(reverse('top_6'))

        self.assertContains(response, 'Voir tes produits favoris')
        self.assertContains(response, 'Top 6 des utilisateurs')
        self.assertIs(type(response.context['products']), list)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/favorites.html')

    @patch('product.models.BaseProductManager.get_top_6')
    def test_top_no_result(self, mock_get_top_6):
        
        mock_get_top_6.return_value = []
            
        response = self.client.get(reverse('top_6'))

        self.assertContains(response, 'Top 6 des utilisateurs')
        self.assertContains(response, "Oups, il n'y à pas encore de résultats")

        self.assertIs(type(response.context['products']), list)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/favorites.html')    