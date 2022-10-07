import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from utils.browser import make_chrome_browser


class TestBaseFunctionalTestCase(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser = make_chrome_browser()
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def sleep(self, time_sleep=5):
        time.sleep(5)


class TestRecipeHomePageFunctionalTestCase(TestBaseFunctionalTestCase):
    def test_the_test(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('Nada por aqui ainda', body.text)
