from django.core.exceptions import ValidationError

from .test_recipe_base import RecipeSetup


class RecipeModelTest(RecipeSetup):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    # Teste será válido se quando no campo title o valor dele
    #  passar do max_length e subir uma exceção de ValidationError
    def test_recipe_title_raises_error_if_title_has_more_than_65_chars(self):
        self.recipe.title = "A" * 70

        # Usando o context manager é esperado a exception no bloco de código
        with self.assertRaises(ValidationError):
            # Usando o full_clean é possivel ter a validação dos campos
            # Caso o valor ñ atenda os paramethers do campo
            #  ele sobe a exception ValidationError
            self.recipe.full_clean()
