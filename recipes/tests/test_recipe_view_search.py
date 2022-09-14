from django.urls import resolve, reverse
from recipes import views

from .test_recipe_base import RecipeSetup


class RecipeViewSeachTest(RecipeSetup):
    # SEARCH
    # Conferir se a view esta correta
    def test_check_recipe_view_search_is_correct(self):
        response = resolve(reverse('recipes:search'))
        self.assertIs(response.func, views.search)

    def test_check_loads_search_correct_template(self):
        response = self.client.get(
            reverse('recipes:search') + ('?search=Teste'))
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_check_return_404_if_not_query_in_search(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertEqual(response.status_code, 404)

    def test_check_page_title_is_escaped(self):
        url = reverse('recipes:search') + '?search=<Teste>'
        response = self.client.get(url)
        self.assertIn('Search for &quot;&lt;Teste&gt;&quot;',
                      response.content.decode('utf-8'))
