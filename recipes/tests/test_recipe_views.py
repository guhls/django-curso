from django.test import TestCase
from django.urls import reverse, resolve
from recipes import views
from recipes.models import Category, Recipe
from django.contrib.auth.models import User


class RecipeViewsTest(TestCase):
    # HOME
    # Teste Para verificar se esta caregando a view esperada
    def test_recipe_home_view_ok(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    # Fazer um teste que verifique se retorna o status code de 200 na view
    def test_check_status_200_view_home(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    # Fazer um teste que verifique qual template é usado na view
    def test_check_template_view_home(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    # Fazer um teste que verifique o que retorna quando não há recipe
    def test_check_template_not_found_view_home(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            'Nada por aqui ainda',
            response.content.decode('utf-8')
        )

    # Fazer um teste para verificar se carega os recipes
    def test_check_templates_loads_in_home(self):
        author = User.objects.create_user(
            first_name='user',
            last_name='name',
            username='username',
            password='123',
            email='username@email.com'
        )
        category = Category.objects.create(name='Category')

        Recipe.objects.create(
            author=author,
            category=category,
            title='Recipe Title',
            description='Description title',
            slug='slug-recipe',
            preparation_time=20,
            preparation_time_unit='Minutos',
            servings=4,
            servings_unit='Pessoas',
            preparation_steps='Preparo',
            preparation_steps_is_html=False,
            is_published=True,
        )

        response = self.client.get(reverse('recipes:home'))
        response_recipes = response.context['recipes']
        content = response.content.decode('utf-8')

        self.assertEqual(response_recipes.first().title, 'Recipe Title')
        self.assertIn('Recipe Title', content)
        self.assertEqual(len(response_recipes), 1)

    # CATEGORY
    # Teste Para verificar se esta caregando a view esperada
    def test_recipe_category_view_ok(self):
        view = resolve('/recipes/category/1/')
        self.assertIs(view.func, views.category)

    # Fazer um teste que verifique se retorna o status code de 200 na view
    def test_check_status_404_view_category(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000})
            )
        self.assertEqual(response.status_code, 404)

    # RECIPE
    # Teste Para verificar se esta caregando a view esperada
    def test_recipe_view_ok(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    # Fazer um teste que verifique se retorna o status code de 200 na view
    def test_check_status_404_view_recipe(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1000})
            )
        self.assertEqual(response.status_code, 404)
