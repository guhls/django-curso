from django.urls import resolve, reverse
from recipes import views

from .test_recipe_base import RecipeSetup

#  from unittest import skip


class RecipeViewsTest(RecipeSetup):
    # HOME
    # Teste Para verificar se esta caregando a view esperada
    def test_recipe_home_view_ok(self):
        view = resolve(reverse("recipes:home"))
        self.assertIs(view.func, views.home)

    # Fazer um teste que verifique se retorna o status code de 200 na view
    def test_check_status_200_view_home(self):
        response = self.client.get(reverse("recipes:home"))
        self.assertEqual(response.status_code, 200)

    # Fazer um teste que verifique qual template é usado na view
    def test_check_template_view_home(self):
        response = self.client.get(reverse("recipes:home"))
        self.assertTemplateUsed(response, "recipes/pages/home.html")

    # Fazer um teste que verifique o que retorna quando não há recipe
    #  @skip('WIP')
    def test_check_template_not_found_view_home(self):
        response = self.client.get(reverse("recipes:home"))
        self.assertIn("Nada por aqui ainda", response.content.decode("utf-8"))

        #  self.fail()

    # Fazer um teste para verificar se carega os recipes
    def test_check_recipes_loads_in_home(self):
        self.make_recipe()

        response = self.client.get(reverse("recipes:home"))
        response_recipes = response.context["recipes"]
        content = response.content.decode("utf-8")

        self.assertEqual(response_recipes.first().title, "Recipe Title")
        self.assertIn("Recipe Title", content)
        self.assertEqual(len(response_recipes), 1)

    # Teste que verifica o que retorna quando a recipe não esta publicada
    def test_check_recipe_not_published_in_home(self):
        self.make_recipe(is_published=False)

        response = self.client.get(reverse("recipes:home"))
        self.assertIn("Nada por aqui ainda", response.content.decode("utf-8"))

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
