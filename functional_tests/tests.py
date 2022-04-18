from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from django.test import LiveServerTestCase
import unittest
import os
import time


MAX_TIME = 5

class NewVisitorTest(LiveServerTestCase):
   
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
                rows = table.find_elements(By.TAG_NAME, 'tr')

                self.assertIn(
                    text, 
                    [row.text for row in rows]
                )
                return 
            except (WebDriverException, AssertionError) as e:
                if time.time() - START_TIME > MAX_TIME:
                    raise e
                else:
                    time.sleep(0.2)


    def test_start_services_and_retrieve_it_later(self):
        self.browser.get(self.live_server_url)

        self.assertIn("静网", self.browser.title)
        header = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn("静网", header)

        category_inputbox = self.browser.find_element(By.ID, 'id_new_category_name')
        self.assertEqual(
            category_inputbox.get_attribute('placeholder'),
            "服务类型"
        )
        category_abbr_inputbox = self.browser.find_element(By.ID, 'id_new_category_name_abbr')
        self.assertEqual(
            category_abbr_inputbox.get_attribute('placeholder'),
            "服务类型缩写"
        )
        service_inputbox = self.browser.find_element(By.ID, 'id_new_service_name')
        self.assertEqual(
            service_inputbox.get_attribute('placeholder'),
            "服务名"
        )
        submit = self.browser.find_element(By.ID, 'id_submit')
        self.assertEqual(
            submit.get_attribute('value'),
            "提交"
        )


        category_inputbox.send_keys("Virtual Private Network")
        category_abbr_inputbox.send_keys("VPN")
        service_inputbox.send_keys("pptpd")
        submit.click()

        self.wait_to_check_text_in_table('1. pptpd')

        
        inputbox = self.browser.find_element(By.ID, 'id_new_service_name')
        submit = self.browser.find_element(By.ID, 'id_submit')
        inputbox.send_keys("xl2tpd")
        submit.click()

        self.wait_to_check_text_in_table('2. xl2tpd')
        self.wait_to_check_text_in_table('1. pptpd')

    def test_start_multiple_types_of_service_at_diffent_urls(self):
        self.browser.get(self.live_server_url)

        inputbox = self.browser.find_element(By.ID, 'id_new_service_name')
        submit = self.browser.find_element(By.ID, 'id_submit')
        inputbox.send_keys("pptpd")
        submit.click()

        self.wait_to_check_text_in_table('1. pptpd')
        VPN_URL = self.browser.current_url
        self.assertRegex(VPN_URL, '/services/.+/')

        self.browser.quit()
        self.setUp()

        self.browser.get(self.live_server_url)
        page = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('pptpd', page)

        inputbox = self.browser.find_element(By.ID, 'id_new_service_name')
        submit = self.browser.find_element(By.ID, 'id_submit')
        inputbox.send_keys("nps")
        submit.click()

        self.wait_to_check_text_in_table('1. nps')
        TUNNEL_URL = self.browser.current_url
        self.assertRegex(VPN_URL, '/services/.+/')
        self.assertNotEqual(TUNNEL_URL, VPN_URL)

        page = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('pptpd', page)

        self.browser.get(self.live_server_url)
        page = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('pptpd', page)
        self.assertIn('nps', page)
        

