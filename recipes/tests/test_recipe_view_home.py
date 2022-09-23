from django.urls import resolve, reverse
from recipes import views

from .test_recipe_base import RecipeSetup

#  from unittest import skip


class RecipeViewHomeTest(RecipeSetup):
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
        response_recipes = response.context["recipes"].object_list
        content = response.content.decode("utf-8")

        self.assertEqual(response_recipes[0].title, "Recipe Title")
        self.assertIn("Recipe Title", content)
        self.assertEqual(len(response_recipes), 1)

    # Teste que verifica o que retorna quando a recipe não esta publicada
    def test_check_recipe_not_published_in_home(self):
        self.make_recipe(is_published=False)

        response = self.client.get(reverse("recipes:home"))
        self.assertIn("Nada por aqui ainda", response.content.decode("utf-8"))

    # Teste para validar se o pagination retorna as recipes esperadas
    def test_check_paginator_is_correct(self):
        r = self.make_recipe()
        for i in range(12):
            r.id = None
            r.slug = f'title-{i}'
            r.save()

        response1 = self.client.get(reverse('recipes:home'))
        response2 = self.client.get(reverse('recipes:home')+'?page=3')

        self.assertEqual(len(response1.context['recipes'].object_list), 6)
        self.assertEqual(len(response2.context['recipes'].object_list), 1)
