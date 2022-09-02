from django.test import TestCase

from recipes.models import Category, Recipe
from django.contrib.auth.models import User


class RecipeSetup(TestCase):
    def setUp(self) -> None:
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
        return super().setUp()
