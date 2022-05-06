from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from .base import FunctionalTest

class LayoutAndStylingTest(FunctionalTest):

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

