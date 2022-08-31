from django.test import TestCase
from django.urls import reverse


class RecipeURLsTest(TestCase):
    def test_recipe_home_url_is_ok(self):
        home_url = reverse('recipes:home')
        self.assertEqual(home_url, '/recipes/')

    def test_category_url_ok(self):
        category_url = reverse('recipes:category', args=(1, ))
        self.assertEqual(category_url, '/recipes/category/1/')

    def test_recipe_url_ok(self):
        category_url = reverse('recipes:recipe', kwargs={'id': 1})
        self.assertEqual(category_url, '/recipes/1/')
