from django.urls import resolve, reverse
from recipes import views

from .test_recipe_base import RecipeSetup


class RecipeViewDetailTest(RecipeSetup):
    # DETAIL
    # Teste Para verificar se esta caregando a view esperada

    def test_recipe_view_ok(self):
        view = resolve(reverse("recipes:recipe", kwargs={"id": 1}))
        self.assertIs(view.func, views.recipe)

    # Fazer um teste que verifique se retorna o status code de 200 na view
    def test_check_status_404_view_recipe(self):
        response = self.client.get(
            reverse("recipes:recipe", kwargs={"id": 1000}))
        self.assertEqual(response.status_code, 404)

    # Fazer um teste para verificar se carega a recipe
    def test_check_recipe_detail_loads_in_recipe_view(self):
        needed_title = "Title recipe in Recipe View - One Recipe Detail"

        self.make_recipe(title=needed_title)

        response = self.client.get(reverse("recipes:recipe", args=(1,)))
        content = response.content.decode("utf-8")

        self.assertIn(needed_title, content)

    # Teste para verificar o que retorna com recipe not published
    def test_check_recipe_detail_not_published(self):
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(
            reverse("recipes:recipe", kwargs={"id": recipe.id}))

        self.assertEqual(response.status_code, 404)
