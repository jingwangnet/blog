from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import unittest
import os
import time


MAX_TIME = 5

class FunctionalTest(StaticLiveServerTestCase):
   
    def setUp(self):
        if os.environ.get('HEADLESS', False):
            options = Options()
            options.headless = True
            self.browser = webdriver.Chrome(options=options)
        else:
            self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def wait_to_check_text_in_table(self, text):
        START_TIME = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, 'id_service_table')
                articles = table.find_elements(By.TAG_NAME, 'article')

                self.assertIn(
                    text, 
                    [article.find_element(By.TAG_NAME, 'h1').text for article in articles]
                )
                return 
            except (WebDriverException, AssertionError) as e:
                if time.time() - START_TIME > MAX_TIME:
                    raise e
                else:
                    time.sleep(0.2)


    def check_text_in_page(self, text ):
        page = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn(
            text,
            page
        )



