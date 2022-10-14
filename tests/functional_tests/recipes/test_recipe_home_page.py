import pytest
from selenium.webdriver.common.by import By

from .base import TestBaseFunctionalTestCase


@pytest.mark.functional_test
class TestRecipeHomePageFunctionalTestCase(TestBaseFunctionalTestCase):
    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('Nada por aqui ainda', body.text)

    def test_recipe_search_page_within_recipe(self):
        self.browser.get(self.live_server_url +
                         '/recipes/search/?search=Teste')
        self.sleep()
        body = self.browser.find_element(By.CLASS_NAME, 'search-h1')
        self.assertIn("Nada por aqui ainda", body.text)
