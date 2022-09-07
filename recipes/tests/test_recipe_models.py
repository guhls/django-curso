from django.core.exceptions import ValidationError
from parameterized import parameterized

from .test_recipe_base import Recipe, RecipeSetup


class RecipeModelTest(RecipeSetup):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def make_recipe_default(self):
        recipe = Recipe(
            author=self.make_author(username='NewUser'),
            category=self.make_category(
                name='Category preparation_steps'),
            title='Title for preparation_steps',
            description='Description',
            slug='slug-recipe',
            preparation_time=20,
            preparation_time_unit='Minutos',
            servings=4,
            servings_unit='Pessoas',
            preparation_steps='Preparo',
        )

        recipe.full_clean()
        recipe.save()

        return recipe

    # Teste será válido se quando no campo title o valor dele
    #  passar do max_length e subir uma exceção de ValidationError
    # def test_recipe_title_raises_error_if_title_has_more_than_65_chars(self):
        # self.recipe.title = "A" * 70

        # # Usando o context manager é esperado a exception no bloco de código
        # with self.assertRaises(ValidationError):
        #     # Usando o full_clean é possivel ter a validação dos campos
        #     # Caso o valor ñ atenda os paramethers do campo
        #     #  ele sobe a exception ValidationError
        #     self.recipe.full_clean()

    # Os testes serão criados aqui o def test_recipe_max_length náo é um test
    #   ele é um agrupador de testes que serão criados com a parametrização
    # @parameterized.expand é usado pois a classe é herdada do TestCase
    @parameterized.expand(
        [
            ("title", 65),
            ("description", 165),
            ("preparation_time_unit", 65),
            ("servings_unit", 65),
        ]
    )
    def test_recipe_max_length(self, field, max_length):
        setattr(self.recipe, field, "A" * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    def test_recipe_preparation_steps_is_html_is_false_by_default(self):
        recipe = self.make_recipe_default()

        self.assertFalse(
            recipe.preparation_steps_is_html,
            msg='preparation_steps_is_html is not False by default'
        )

    def test_recipe_is_published_is_false_by_default(self):
        recipe = self.make_recipe_default()

        self.assertFalse(
            recipe.is_published,
            msg='is_published is not False by default'
        )
