from django.core.exceptions import ValidationError

from .test_recipe_base import RecipeSetup


class RecipeModelTest(RecipeSetup):
    def setUp(self) -> None:
        self.category = self.make_category()
        return super().setUp()

    def test_recipe_category_string_representation_is_name_field(self):
        self.category.name = 'Category Representation Field'
        self.assertEqual(str(self.category), 'Category Representation Field')

    def test_check_cateory_name_field_if_max_length_is_65_chars(self):
        self.category.name = 'A' * 66
        with self.assertRaises(ValidationError):
            self.category.full_clean()
