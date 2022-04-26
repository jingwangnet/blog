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

class NewVisitorTest(StaticLiveServerTestCase):
   
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



    def test_start_services_and_retrieve_it_later(self):
        self.browser.get(self.live_server_url)

        ## title and header
        self.assertIn("静网", self.browser.title)
        header = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn("服务列表", header)

        ## placeholder
        category_name_inputbox = self.browser.find_element(By.ID, 'id_new_category_name')
        self.assertEqual(
            category_name_inputbox.get_attribute('placeholder'),
            "服务类型名"
        )
        category_abbr_inputbox = self.browser.find_element(By.ID, 'id_new_category_abbr')
        self.assertEqual(
            category_abbr_inputbox.get_attribute('placeholder'),
            "服务类型名缩写"
        )
        category_resume_textarea = self.browser.find_element(By.ID, 'id_new_category_resume')
        self.assertEqual(
            category_resume_textarea.get_attribute('placeholder'),
            "服务类型简介"
        )
        service_name_inputbox = self.browser.find_element(By.ID, 'id_new_service_name')
        self.assertEqual(
            service_name_inputbox.get_attribute('placeholder'),
            "服务名"
        )
        service_abbr_inputbox = self.browser.find_element(By.ID, 'id_new_service_abbr')
        self.assertEqual(
            service_abbr_inputbox.get_attribute('placeholder'),
            "服务名缩写"
        )
        service_resume_textarea = self.browser.find_element(By.ID, 'id_new_service_resume')
        self.assertEqual(
            service_resume_textarea.get_attribute('placeholder'),
            "服务简介"
        )
        submit = self.browser.find_element(By.ID, 'id_submit')
        self.assertEqual(
            submit.get_attribute('value'),
            "提交"
        )

        category_name_inputbox.send_keys("Virtual Private Network")
        category_abbr_inputbox.send_keys("VPN")
        category_resume_textarea.send_keys("vpn resume")
        service_name_inputbox.send_keys("pptpd")
        service_abbr_inputbox.send_keys("pptpd abbr")
        service_resume_textarea.send_keys("pptpd resume")
        submit.send_keys(Keys.ENTER)

        self.wait_to_check_text_in_table('1. pptpd')
        self.check_text_in_page("pptpd abbr")
        self.check_text_in_page("pptpd resume")
        self.check_text_in_page("Virtual Private Network")
        self.check_text_in_page("VPN")
        self.check_text_in_page("vpn resume")

        service_name_inputbox = self.browser.find_element(By.ID, 'id_new_service_name')
        service_abbr_inputbox = self.browser.find_element(By.ID, 'id_new_service_abbr')
        service_resume_textarea = self.browser.find_element(By.ID, 'id_new_service_resume')
        submit = self.browser.find_element(By.ID, 'id_submit')
        service_name_inputbox.send_keys("xl2tpd")
        service_abbr_inputbox.send_keys("xl2tpd abbr")
        service_resume_textarea.send_keys("xl2tpd resume")
        submit.send_keys(Keys.ENTER)

        self.wait_to_check_text_in_table('2. xl2tpd')
        self.wait_to_check_text_in_table('1. pptpd')
        self.check_text_in_page("xl2tpd resume")
        self.check_text_in_page("xl2tpd abbr")
        self.check_text_in_page("pptpd resume")
        self.check_text_in_page("pptpd abbr")

    def test_start_multiple_types_of_service_at_diffent_urls(self):
        self.browser.get(self.live_server_url)

        page = self.browser.find_element(By.TAG_NAME, 'body').text
        self.check_text_in_page('服务列表')
        self.check_text_in_page('还有添加服务!')

        category_name_inputbox = self.browser.find_element(By.ID, 'id_new_category_name')
        category_abbr_inputbox = self.browser.find_element(By.ID, 'id_new_category_abbr')
        category_resume_textarea = self.browser.find_element(By.ID, 'id_new_category_resume')
        service_name_inputbox = self.browser.find_element(By.ID, 'id_new_service_name')
        service_abbr_inputbox = self.browser.find_element(By.ID, 'id_new_service_abbr')
        service_resume_textarea = self.browser.find_element(By.ID, 'id_new_service_resume')
        submit = self.browser.find_element(By.ID, 'id_submit')

        category_name_inputbox.send_keys("Virtual Private Network")
        category_abbr_inputbox.send_keys("VPN")
        category_resume_textarea.send_keys("vpn resume")
        service_name_inputbox.send_keys("pptpd")
        service_abbr_inputbox.send_keys("pptpd abbr")
        service_resume_textarea.send_keys("pptpd resume")
        submit.send_keys(Keys.ENTER)

        VPN_URL = self.browser.current_url
        self.assertRegex(VPN_URL, '/services/[^0-9]+/')

        self.wait_to_check_text_in_table('1. pptpd')
        self.check_text_in_page("pptpd abbr")
        self.check_text_in_page("pptpd resume")
        self.check_text_in_page("Virtual Private Network")
        self.check_text_in_page("VPN")
        self.check_text_in_page("vpn resume")

        self.browser.quit()
        self.setUp()

        self.browser.get(self.live_server_url)
        
        self.check_text_in_page('服务列表')
        self.check_text_in_page('Virtual Private Network')
        self.check_text_in_page('vpn resume')
        self.check_text_in_page('1. pptpd')
        self.check_text_in_page('pptpd abbr')
        self.check_text_in_page('pptpd resume')

        category_name_inputbox = self.browser.find_element(By.ID, 'id_new_category_name')
        category_abbr_inputbox = self.browser.find_element(By.ID, 'id_new_category_abbr')
        category_resume_textarea = self.browser.find_element(By.ID, 'id_new_category_resume')
        service_name_inputbox = self.browser.find_element(By.ID, 'id_new_service_name')
        service_abbr_inputbox = self.browser.find_element(By.ID, 'id_new_service_abbr')
        service_resume_textarea = self.browser.find_element(By.ID, 'id_new_service_resume')
        submit = self.browser.find_element(By.ID, 'id_submit')
       
        category_name_inputbox.send_keys("NAT traversal")
        category_abbr_inputbox.send_keys("内网穿透")
        category_resume_textarea.send_keys("nat traversal resume")
        service_name_inputbox.send_keys("nps")
        category_abbr_inputbox.send_keys("nps abbr")
        service_resume_textarea.send_keys("nps resume")
        submit.send_keys(Keys.ENTER)

        self.wait_to_check_text_in_table('1. nps')
        self.check_text_in_page("NAT traversal")
        self.check_text_in_page("内网穿透")
        self.check_text_in_page("nat traversal resume")
        self.check_text_in_page("nps abbr")
        self.check_text_in_page("nps resume")

        TUNNEL_URL = self.browser.current_url
        self.assertRegex(VPN_URL, '/services/[^0-9]+/')
        self.assertNotEqual(TUNNEL_URL, VPN_URL)

        page = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('pptpd', page)

        home_link = self.browser.find_element(By.LINK_TEXT, '静网')
        home_link.click()
        #self.browser.get(self.live_server_url)
        self.check_text_in_page('服务列表')
        self.check_text_in_page('Virtual Private Network')
        self.check_text_in_page('vpn resume')
        self.check_text_in_page('1. pptpd')
        self.check_text_in_page('pptpd abbr')
        self.check_text_in_page('pptpd resume')
        self.check_text_in_page('NAT traversal')
        self.check_text_in_page('nat traversal resume')
        self.check_text_in_page('1. nps')
        self.check_text_in_page('nps abbr')
        self.check_text_in_page('nps resume')

        vpn_link = self.browser.find_element(By.LINK_TEXT, 'Virtual Private Network')
        vpn_link.click()
        self.wait_to_check_text_in_table('1. pptpd')
        self.check_text_in_page("Virtual Private Network")
        self.check_text_in_page("VPN")
        self.check_text_in_page("vpn resume")

    def test_layout_and_styling(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(768, 1000)

        category_name_inputbox = self.browser.find_element(By.ID, 'id_new_category_name')
        category_abbr_inputbox = self.browser.find_element(By.ID, 'id_new_category_abbr')
        category_resume_textarea = self.browser.find_element(By.ID, 'id_new_category_resume')
        service_name_inputbox = self.browser.find_element(By.ID, 'id_new_service_name')
        service_abbr_inputbox = self.browser.find_element(By.ID, 'id_new_service_abbr')
        service_resume_textarea = self.browser.find_element(By.ID, 'id_new_service_resume')
        submit = self.browser.find_element(By.ID, 'id_submit')

        self.assertAlmostEqual(
             service_name_inputbox.size['width'] / 768,
             0.9,
             delta=0.2
        )
        
        category_name_inputbox.send_keys("Virtual Private Network")
        category_abbr_inputbox.send_keys("VPN")
        category_resume_textarea.send_keys("vpn resume")
        service_name_inputbox.send_keys("pptpd")
        service_abbr_inputbox.send_keys("pptpd abbr")
        service_resume_textarea.send_keys("pptpd resume")
        submit.send_keys(Keys.ENTER)

        self.wait_to_check_text_in_table('1. pptpd')

        service_name_inputbox = self.browser.find_element(By.ID, 'id_new_service_name')
        self.assertAlmostEqual(
             service_name_inputbox.size['width'] / 768,
             0.9,
             delta=0.2
        )
