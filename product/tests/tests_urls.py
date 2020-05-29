from django.test import TestCase, Client
from django.urls import resolve, reverse


class TestUrls(TestCase):

    def test_legals_url(self): 
        resolver_match = resolve('/legals/')
        self.assertEqual(
            resolver_match.func.__name__,
            'legals'
            )
    
    def test_products_url(self): 
        resolver_match = resolve('/products/')
        self.assertEqual(
            resolver_match.func.__name__,
            'results'
            )

    def test_food_url(self): 
        resolver_match = resolve('/food/')
        self.assertEqual(
            resolver_match.func.__name__,
            'food'
            )

    def test_favorites_url(self): 
        resolver_match = resolve('/favorites/')
        self.assertEqual(
            resolver_match.func.__name__,
            'favorites'
            )

    def test_change_favorite_url(self): 
        resolver_match = resolve('/favorites/change/')
        self.assertEqual(
            resolver_match.func.__name__,
            'change_favorite'
            )
    
    def test_top_6_url(self): 
        resolver_match = resolve('/favorites/top')
        self.assertEqual(
            resolver_match.func.__name__,
            'top_6'
            )
