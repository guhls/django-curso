from django.urls import resolve, reverse
from recipes import views

from .test_recipe_base import RecipeSetup

#  from unittest import skip


class RecipeViewCategoryTest(RecipeSetup):
    # CATEGORY
    # Teste Para verificar se esta caregando a view esperada
    def test_recipe_category_view_ok(self):
        view = resolve("/recipes/category/1/")
        self.assertIs(view.func, views.category)

    # Fazer um teste que verifique se retorna o status code de 200 na view
    def test_check_status_404_view_category(self):
        response = self.client.get(
            reverse("recipes:category", kwargs={"category_id": 1000})
        )
        self.assertEqual(response.status_code, 404)

    # Fazer um teste para verificar se carega os recipes na category
    def test_check_recipes_loads_in_category(self):
        needed_title = "Title recipe in Category"

        self.make_recipe(title=needed_title)

        response = self.client.get(
            reverse("recipes:category", kwargs={"category_id": 1})
        )
        content = response.content.decode("utf-8")

        self.assertIn(needed_title, content)

    # Teste para verificar o que retorna em category com recipe not published
    def test_check_recipe_not_published_in_category(self):
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(
            reverse("recipes:category", kwargs={
                    "category_id": recipe.category.id})
        )

        self.assertEqual(response.status_code, 404)
