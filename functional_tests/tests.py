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

    def check_text_in_dl(self, element, text):
        dl = self.browser.find_element(By.ID, 'id_service_table')
        rows = dl.find_elements(By.TAG_NAME, element)

        self.assertIn(
            text, 
            [row.text for row in rows]
        )

    def check_text_in_page(self, text ):
        page = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn(
            text,
            page
        )



    def test_start_services_and_retrieve_it_later(self):
        self.browser.get(self.live_server_url)

        self.assertIn("静网", self.browser.title)
        header = self.browser.find_element(By.TAG_NAME, 'h1').text
        self.assertIn("静网", header)

        category_inputbox = self.browser.find_element(By.ID, 'id_new_category_name')
        self.assertEqual(
            category_inputbox.get_attribute('placeholder'),
            "服务类型名"
        )
        category_abbr_inputbox = self.browser.find_element(By.ID, 'id_new_category_abbr')
        self.assertEqual(
            category_abbr_inputbox.get_attribute('placeholder'),
            "服务类型名缩写"
        )
        category_resume_inputbox = self.browser.find_element(By.ID, 'id_new_category_resume')
        self.assertEqual(
            category_resume_inputbox.get_attribute('placeholder'),
            "服务类型简介"
        )
        service_inputbox = self.browser.find_element(By.ID, 'id_new_service_name')
        self.assertEqual(
            service_inputbox.get_attribute('placeholder'),
            "服务名"
        )
        service_resume_inputbox = self.browser.find_element(By.ID, 'id_new_service_resume')
        self.assertEqual(
            service_resume_inputbox.get_attribute('placeholder'),
            "服务简介"
        )
        submit = self.browser.find_element(By.ID, 'id_submit')
        self.assertEqual(
            submit.get_attribute('value'),
            "提交"
        )

        category_inputbox.send_keys("Virtual Private Network")
        category_abbr_inputbox.send_keys("VPN")
        category_resume_inputbox.send_keys("将专用网络延伸到公共网络上，使用户能够在共享或公共网络上发送和接收数据，就像他们的计算设备直接连接到专用网络上一样[1]。VPN的好处包括增加专用网络的功能、安全性和管理，它提供了对公共网络上无法访问的资源访问通常用于远程办公人员。加密很常见但不是VPN连接的固有部分。")
        service_inputbox.send_keys("pptpd")
        service_resume_inputbox.send_keys("点对点隧道协议(PPTP)是一种实现虚拟专用网(VPN)的方法。PPTP 在TCP之上使用一个控制通道和 GRE 隧道操作加密 PPP 数据包")
        submit.click()

        self.wait_to_check_text_in_table('1. pptpd')
        self.check_text_in_page("Virtual Private Network")
        self.check_text_in_page("VPN")
        self.check_text_in_page("将专用网络延伸到公共网络上，使用户能够在共享或公共网络上发送和接收数据，就像他们的计算设备直接连接到专用网络上一样[1]。VPN的好处包括增加专用网络的功能、安全性和管理，它提供了对公共网络上无法访问的资源访问通常用于远程办公人员。加密很常见但不是VPN连接的固有部分。")
        
        inputbox = self.browser.find_element(By.ID, 'id_new_service_name')
        submit = self.browser.find_element(By.ID, 'id_submit')
        inputbox.send_keys("xl2tpd")
        submit.click()

        self.wait_to_check_text_in_table('2. xl2tpd')
        self.wait_to_check_text_in_table('1. pptpd')

    def test_start_multiple_types_of_service_at_diffent_urls(self):
        self.browser.get(self.live_server_url)

        page = self.browser.find_element(By.TAG_NAME, 'body').text
        self.check_text_in_page('服务列表')
        self.check_text_in_page('还有添加服务!')

        category_inputbox = self.browser.find_element(By.ID, 'id_new_category_name')
        category_abbr_inputbox = self.browser.find_element(By.ID, 'id_new_category_abbr')
        category_resume_inputbox = self.browser.find_element(By.ID, 'id_new_category_resume')
        service_inputbox = self.browser.find_element(By.ID, 'id_new_service_name')
        submit = self.browser.find_element(By.ID, 'id_submit')

        category_inputbox.send_keys("Virtual Private Network")
        category_abbr_inputbox.send_keys("VPN")
        category_resume_inputbox.send_keys("将专用网络延伸到公共网络上，使用户能够在共享或公共网络上发送和接收数据，就像他们的计算设备直接连接到专用网络上一样[1]。VPN的好处包括增加专用网络的功能、安全性和管理，它提供了对公共网络上无法访问的资源访问通常用于远程办公人员。加密很常见但不是VPN连接的固有部分。")
        service_inputbox.send_keys("pptpd")
        submit.click()

        VPN_URL = self.browser.current_url
        self.assertRegex(VPN_URL, '/services/.+/')

        self.wait_to_check_text_in_table('1. pptpd')
        self.check_text_in_page("Virtual Private Network")
        self.check_text_in_page("VPN")
        self.check_text_in_page("将专用网络延伸到公共网络上，使用户能够在共享或公共网络上发送和接收数据，就像他们的计算设备直接连接到专用网络上一样[1]。VPN的好处包括增加专用网络的功能、安全性和管理，它提供了对公共网络上无法访问的资源访问通常用于远程办公人员。加密很常见但不是VPN连接的固有部分。")

        self.browser.quit()
        self.setUp()

        self.browser.get(self.live_server_url)
        
        page = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('pptpd', page)
        self.check_text_in_page('服务列表')
        self.check_text_in_dl('dt', 'Virtual Private Network')
        self.check_text_in_dl('dd', '1. pptpd')

        category_inputbox = self.browser.find_element(By.ID, 'id_new_category_name')
        category_abbr_inputbox = self.browser.find_element(By.ID, 'id_new_category_abbr')
        category_resume_inputbox = self.browser.find_element(By.ID, 'id_new_category_resume')
        service_inputbox = self.browser.find_element(By.ID, 'id_new_service_name')
        submit = self.browser.find_element(By.ID, 'id_submit')

        category_inputbox.send_keys("NAT traversal")
        category_abbr_inputbox.send_keys("内网穿透")
        category_resume_inputbox.send_keys("涉及TCP/IP网络中的一个常见问题，即在处于使用了NAT设备的私有TCP/IP网络中的主机之间创建连接的问题。")
        service_inputbox.send_keys("nps")
        submit.click()

        self.wait_to_check_text_in_table('1. nps')
        self.check_text_in_page("NAT traversal")
        self.check_text_in_page("内网穿透")
        self.check_text_in_page("涉及TCP/IP网络中的一个常见问题，即在处于使用了NAT设备的私有TCP/IP网络中的主机之间创建连接的问题。")

        TUNNEL_URL = self.browser.current_url
        self.assertRegex(VPN_URL, '/services/.+/')
        self.assertNotEqual(TUNNEL_URL, VPN_URL)

        page = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('pptpd', page)

        home_link = self.browser.find_element(By.LINK_TEXT, '静网')
        home_link.click()
        #self.browser.get(self.live_server_url)
        page = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertIn('pptpd', page)
        self.assertIn('nps', page)
        self.check_text_in_page('服务列表')
        self.check_text_in_dl('dt', 'Virtual Private Network')
        self.check_text_in_dl('dd', '1. pptpd')
        self.check_text_in_dl('dt', 'NAT traversal')
        self.check_text_in_dl('dd', '1. nps')

        
        vpn_link = self.browser.find_element(By.LINK_TEXT, 'Virtual Private Network')
        vpn_link.click()
        self.wait_to_check_text_in_table('1. pptpd')
        self.check_text_in_page("Virtual Private Network")
        self.check_text_in_page("VPN")
        self.check_text_in_page("将专用网络延伸到公共网络上，使用户能够在共享或公共网络上发送和接收数据，就像他们的计算设备直接连接到专用网络上一样[1]。VPN的好处包括增加专用网络的功能、安全性和管理，它提供了对公共网络上无法访问的资源访问通常用于远程办公人员。加密很常见但不是VPN连接的固有部分。")

    def test_layout_and_styling(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(768, 1000)

        category_inputbox = self.browser.find_element(By.ID, 'id_new_category_name')
        category_abbr_inputbox = self.browser.find_element(By.ID, 'id_new_category_abbr')
        category_resume_inputbox = self.browser.find_element(By.ID, 'id_new_category_resume')
        service_inputbox = self.browser.find_element(By.ID, 'id_new_service_name')
        submit = self.browser.find_element(By.ID, 'id_submit')

        self.assertAlmostEqual(
             service_inputbox.size['width'] / 768,
             0.7,
             delta=0.1
        )
        
        category_inputbox.send_keys("Virtual Private Network")
        category_abbr_inputbox.send_keys("VPN")
        category_resume_inputbox.send_keys("将专用网络延伸到公共网络上，使用户能够在共享或公共网络上发送和接收数据，就像他们的计算设备直接连接到专用网络上一样[1]。VPN的好处包括增加专用网络的功能、安全性和管理，它提供了对公共网络上无法访问的资源访问通常用于远程办公人员。加密很常见但不是VPN连接的固有部分。")
        service_inputbox.send_keys("pptpd")
        submit.click()

        self.wait_to_check_text_in_table('1. pptpd')

        inputbox = self.browser.find_element(By.ID, 'id_new_service_name')
        self.assertAlmostEqual(
             inputbox.size['width'] / 768,
             0.7,
             delta=0.1
        )
