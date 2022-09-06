from django.core.exceptions import ValidationError
from parameterized import parameterized

from .test_recipe_base import RecipeSetup


class RecipeModelTest(RecipeSetup):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

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
