from django.test import TestCase
from django.http import HttpRequest
from django.urls import resolve
from .views import home_page
from .models import Service, Category

# Create your tests here.
class HomePageTest(TestCase):
    
    def test_use_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_display_all_items(self):
        category = Category.objects.create()
        Service.objects.create(name="pptpd", category=category)
        Service.objects.create(name="xl2ptd", category=category)

        response = self.client.get('/')
        self.assertContains(response, 'pptpd')
        self.assertContains(response, 'xl2ptd')


class NewCategoryTest(TestCase):

    data = {
        'new_service': 'pptpd',
        'new_service_resume': '点对点隧道协议(PPTP)是一种实现虚拟专用网(VPN)的方法。PPTP 在TCP之上使用一个控制通道和 GRE 隧道操作加密 PPP 数据包',
        'new_category': 'Virtual Private Network',
        'new_category_abbr': 'VPN',
        'new_category_resume': '将专用网络延伸到公共网络上，使用户能够在共享或公共网络上发送和接收数据，就像他们的计算设备直接连接到专用网络上一样[1]。VPN的好处包括增加专用网络的功能、安全性和管理，它提供了对公共网络上无法访问的资源访问通常用于远程办公人员。加密很常见但不是VPN连接的固有部分。'
    }

    def test_can_save_a_post_request(self):
        response = self.client.post('/services/new', data=self.data)
     
        self.assertEqual(1, Service.objects.count())
        service = Service.objects.first()
        self.assertEqual(service.name, 'pptpd')
        self.assertEqual(service.resume, '点对点隧道协议(PPTP)是一种实现虚拟专用网(VPN)的方法。PPTP 在TCP之上使用一个控制通道和 GRE 隧道操作加密 PPP 数据包')

        self.assertEqual(1, Category.objects.count())
        category = Category.objects.first()
        self.assertEqual(category.name, 'Virtual Private Network')
        self.assertEqual(category.abbr, 'VPN')
        self.assertEqual(category.resume, '将专用网络延伸到公共网络上，使用户能够在共享或公共网络上发送和接收数据，就像他们的计算设备直接连接到专用网络上一样[1]。VPN的好处包括增加专用网络的功能、安全性和管理，它提供了对公共网络上无法访问的资源访问通常用于远程办公人员。加密很常见但不是VPN连接的固有部分。')


    def test_redirect_after_post(self):
        response = self.client.post('/services/new', data=self.data)
        category = Category.objects.first()
         
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], f'/services/{category.pk}/')

class ViewCategoryTest(TestCase):

    def test_use_view_catetory_template(self):
        category = Category.objects.create()
        response = self.client.get(f'/services/{category.pk}/')
        self.assertTemplateUsed(response, 'view_category.html')

    def test_display_only_services_for_that_category(self):
        category_tunnel = Category.objects.create()
        Service.objects.create(name="nps", category=category_tunnel)
        Service.objects.create(name="frp", category=category_tunnel)
        category_vpn = Category.objects.create()
        Service.objects.create(name="pptpd", category=category_vpn)
        Service.objects.create(name="xl2ptd", category=category_vpn)

        response = self.client.get(f'/services/{category_vpn.pk}/')
        self.assertContains(response, 'pptpd')
        self.assertContains(response, 'xl2ptd')
        self.assertNotContains(response, 'nps')
        self.assertNotContains(response, 'frp')

    def test_can_display_categories(self):
        category_vpn = Category.objects.create(
            name = 'Virtual Private Network',
            abbr = 'VPN',
            resume = '将专用网络延伸到公共网络上，使用户能够在共享或公共网络上发送和接收数据，就像他们的计算设备直接连接到专用网络上一样[1]。VPN的好处包括增加专用网络的功能、安全性和管理，它提供了对公共网络上无法访问的资源访问通常用于远程办公人员。加密很常见但不是VPN连接的固有部分。'
        )

        response = self.client.get(f'/services/{category_vpn.pk}/')
        self.assertContains(response, 'Virtual Private Network')
        self.assertContains(response, 'VPN')
        self.assertContains(response, '将专用网络延伸到公共网络上，使用户能够在共享或公共网络上发送和接收数据，就像他们的计算设备直接连接到专用网络上一样[1]。VPN的好处包括增加专用网络的功能、安全性和管理，它提供了对公共网络上无法访问的资源访问通常用于远程办公人员。加密很常见但不是VPN连接的固有部分。'   )

        category_nat = Category.objects.create(
            name = 'NAT traversal',
            abbr = '内网穿透',
            resume = '涉及TCP/IP网络中的一个常见问题，即在处于使用了NAT设备的私有TCP/IP网络中的主机之间创建连接的问题。'
        )
        response = self.client.get(f'/services/{category_nat.pk}/')
        self.assertContains(response, 'NAT traversal')
        self.assertContains(response, '内网穿透')
        self.assertContains(response, '涉及TCP/IP网络中的一个常见问题，即在处于使用了NAT设备的私有TCP/IP网络中的主机之间创建连接的问题。'
        )

    def test_pass_correct_category(self):
        other_category = Category.objects.create()
        category = Category.objects.create()
        response = self.client.get(f'/services/{category.pk}/')

        self.assertEqual(response.context['category'], category)


class AddServicetest(TestCase):

    def test_can_save_a_post_request_to_an_exsiting_category(self):
        other_category = Category.objects.create()
        category = Category.objects.create()
        data = {
            'new_service': 'A service'
        }
        response = self.client.post(f'/services/{category.pk}/add', data=data)
     
        self.assertEqual(1, Service.objects.count())
        service = Service.objects.first()
        self.assertEqual(service.name, 'A service')

    def test_redirect_after_post(self):
        category = Category.objects.create()
        data = {
            'new_service': 'A service'
        }
        response = self.client.post(f'/services/{category.pk}/add', data=data)
         
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], f'/services/{category.pk}/')

class ServiceModelTest(TestCase):

    def test_creating_and_saving_service(self):
        category = Category()
        category.name = 'Virtual Private Network'
        category.abbr = 'VPN'
        category.resume = '将专用网络延伸到公共网络上，使用户能够在共享或公共网络上发送和接收数据，就像他们的计算设备直接连接到专用网络上一样[1]。VPN的好处包括增加专用网络的功能、安全性和管理，它提供了对公共网络上无法访问的资源访问通常用于远程办公人员。加密很常见但不是VPN连接的固有部分。'
        category.save()
        service_1 = Service()
        service_1.name = 'pptpd'
        service_1.category = category 
        service_1.save()
        service_2 = Service()
        service_2.name = 'xl2tpd'
        service_2.category = category
        service_2.save()

        self.assertEqual(2, Service.objects.count())
        self.assertEqual(1, Category.objects.count())

        saved_category = Category.objects.first()

        self.assertEqual(saved_category.name, 'Virtual Private Network')
        self.assertEqual(saved_category.abbr, 'VPN')
        self.assertEqual(saved_category.resume, '将专用网络延伸到公共网络上，使用户能够在共享或公共网络上发送和接收数据，就像他们的计算设备直接连接到专用网络上一样[1]。VPN的好处包括增加专用网络的功能、安全性和管理，它提供了对公共网络上无法访问的资源访问通常用于远程办公人员。加密很常见但不是VPN连接的固有部分。')


        saved_service_1, saved_service_2 = saved_category.service_set.all() 

        self.assertEqual(saved_service_1.name, 'pptpd')
        self.assertEqual(saved_service_1.category, category)
        self.assertEqual(saved_service_2.name, 'xl2tpd')
        self.assertEqual(saved_service_2.category, category)
