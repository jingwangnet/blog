from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import unittest
import os
import time

class NewVisitorTest(unittest.TestCase):
   
    def setUp(self):
        if os.environ.get('HEADLESS', False):
            options = Options()
            options.headless = True
            self.browser = webdriver.Chrome(options=options)
        else:
            self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_start_services_and_retrieve_it_later(self):
        self.browser.get('http://127.0.0.1:8000')

        self.assertIn("静网", self.browser.title)
        header = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn("静网", header)

        inputbox = self.browser.find_element(By.ID, 'id_new_service_name')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            "服务名"
        )
        submit = self.browser.find_element(By.ID, 'id_submit')
        self.assertEqual(
            submit.get_attribute('value'),
            "提交"
        )


        inputbox.send_keys("Poptop")
        submit.click()

        time.sleep(1)

        table = self.browser.find_element(By.ID, 'id_service_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')

        self.assertIn(
            '1. Poptop',
            [row.text for row in rows]
        )
        



if __name__ == '__main__':
    unittest.main()
