from django.test import TestCase
from django.http import HttpRequest
from django.urls import resolve
from .views import home_page
from .models import Service, Category
from django.utils.text import slugify

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
        'new_service_name': 'pptpd',
        'new_service_resume': 'pptpd resume',
        'new_category_name': 'Virtual Private Network',
        'new_category_abbr': 'VPN',
        'new_category_resume': 'VPN resume'
    }

    def test_can_save_a_post_request(self):
        response = self.client.post('/services/new', data=self.data)
     
        self.assertEqual(1, Service.objects.count())
        service = Service.objects.first()
        self.assertEqual(service.name, 'pptpd')
        self.assertEqual(service.resume, 'pptpd resume')

        self.assertEqual(1, Category.objects.count())
        category = Category.objects.first()
        self.assertEqual(category.name, 'Virtual Private Network')
        self.assertEqual(category.abbr, 'VPN')
        self.assertEqual(category.resume, 'VPN resume')


    def test_redirect_after_post(self):
        response = self.client.post('/services/new', data=self.data)
        category = Category.objects.first()
         
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], f'/services/{category.slug}/')

class ViewCategoryTest(TestCase):

    def test_use_view_catetory_template(self):
        category = Category.objects.create()
        response = self.client.get(f'/services/{category.pk}/')
        self.assertTemplateUsed(response, 'view_category.html')

    def test_display_only_services_for_that_category(self):
        category_tunnel = Category.objects.create()
        Service.objects.create(name="nps", resume="resume npns", category=category_tunnel)
        Service.objects.create(name="frp", resume="resume frp", category=category_tunnel)
        category_vpn = Category.objects.create()
        Service.objects.create(name="pptpd", resume="resume pptpd", category=category_vpn)
        Service.objects.create(name="xl2ptd", resume="resume xl2ptd", category=category_vpn)

        response = self.client.get(f'/services/{category_vpn.pk}/')
        self.assertContains(response, 'pptpd')
        self.assertContains(response, 'xl2ptd')
        self.assertContains(response, 'resume pptpd')
        self.assertContains(response, 'resume xl2ptd')
        self.assertNotContains(response, 'nps')
        self.assertNotContains(response, 'frp')
        self.assertNotContains(response, 'resume nps')
        self.assertNotContains(response, 'resume frp')

    def test_can_display_categories(self):
        category_vpn = Category.objects.create(
            name = 'Virtual Private Network',
            abbr = 'VPN',
            resume = 'VPN resume'
        )

        response = self.client.get(f'/services/{category_vpn.pk}/')
        self.assertContains(response, 'Virtual Private Network')
        self.assertContains(response, 'VPN')
        self.assertContains(response, 'VPN resume')

        category_nat = Category.objects.create(
            name = 'NAT traversal',
            abbr = '内网穿透',
            resume = 'NAT resume'
        )
        response = self.client.get(f'/services/{category_nat.pk}/')
        self.assertContains(response, 'NAT traversal')
        self.assertContains(response, '内网穿透')
        self.assertContains(response, 'NAT resume'
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
            'new_service_name': 'A service',
            'new_service_resume': 'A service resume'
        }
        response = self.client.post(f'/services/{category.pk}/add', data=data)
     
        self.assertEqual(1, Service.objects.count())
        service = Service.objects.first()
        self.assertEqual(service.name, 'A service')
        self.assertEqual(service.resume, 'A service resume')

    def test_redirect_after_post(self):
        category = Category.objects.create()
        data = {
            'new_service_name': 'A service',
            'new_service_resume': 'A service resume'
        }
        response = self.client.post(f'/services/{category.pk}/add', data=data)
         
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], f'/services/{category.pk}/')

class ServiceModelTest(TestCase):

    def test_creating_and_saving_service(self):
        category = Category()
        category.name = 'Virtual Private Network'
        category.abbr = 'VPN'
        category.resume = 'VPN resume'
        category.save()

        service_1 = Service()
        service_1.name = 'pptpd'
        service_1.resume = 'pptpd resume'
        service_1.category = category 
        service_1.save()
        service_2 = Service()
        service_2.name = 'xl2tpd'
        service_2.resume = 'xl2tpd resume'
        service_2.category = category
        service_2.save()

        self.assertEqual(2, Service.objects.count())
        self.assertEqual(1, Category.objects.count())

        saved_category = Category.objects.first()

        self.assertEqual(saved_category.name, 'Virtual Private Network')
        self.assertEqual(saved_category.abbr, 'VPN')
        self.assertEqual(saved_category.slug, 'vpn')
        self.assertEqual(saved_category.resume, 'VPN resume')


        saved_service_1, saved_service_2 = saved_category.service_set.all() 

        self.assertEqual(saved_service_1.name, 'pptpd')
        self.assertEqual(saved_service_1.resume, 'pptpd resume')
        self.assertEqual(saved_service_1.category, category)
        self.assertEqual(saved_service_2.name, 'xl2tpd')
        self.assertEqual(saved_service_2.resume, 'xl2tpd resume')
        self.assertEqual(saved_service_2.category, category)
