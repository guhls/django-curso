from django.test import TestCase
from django.urls import reverse, resolve
from . import views


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


class RecipeViewsTest(TestCase):
    def test_recipe_home_view_ok(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_category_view_ok(self):
        view = resolve('/recipes/category/1/')
        self.assertIs(view.func, views.category)

    def test_recipe_view_ok(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)
