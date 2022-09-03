from django.test import TestCase

from recipes.models import Category, Recipe
from django.contrib.auth.models import User


class RecipeSetup(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def make_category(self, name='Category'):
        return Category.objects.create(name='Category')

    def make_author(
        self,
        first_name='user',
        last_name='name',
        username='username',
        password='123',
        email='username@email.com'
    ):
        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email
        )

    def make_recipe(
        self,
        author_data=None,
        category_data=None,
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
    ):
        if author_data is None:
            author_data = {}

        if category_data is None:
            category_data = {}

        return Recipe.objects.create(
            author=self.make_author(**author_data),
            category=self.make_category(**category_data),
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_steps=preparation_steps,
            preparation_steps_is_html=preparation_steps_is_html,
            is_published=is_published,
        )
