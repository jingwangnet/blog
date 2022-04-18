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

    def test_can_save_a_post_request(self):
        data = {
            'new_service': 'A service'
        }
        response = self.client.post('/services/new', data=data)
     
        self.assertEqual(1, Service.objects.count())
        service = Service.objects.first()
        self.assertEqual(service.name, 'A service')

    def test_redirect_after_post(self):
        data = {
            'new_service': 'A service'
        }
        response = self.client.post('/services/new', data=data)
        category = Category.objects.first()
         
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], f'/services/{category.pk}/')

class ViewCategoryTest(TestCase):

    def test_use_view_catetory_template(self):
        category = Category.objects.create()
        response = self.client.get(f'/services/{category.pk}/')
        self.assertTemplateUsed(response, 'view_category.html')

    def test_display_only_services_for_that_category_(self):
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
        saved_service_1, saved_service_2 = saved_category.service_set.all() 

        self.assertEqual(saved_service_1.name, 'pptpd')
        self.assertEqual(saved_service_1.category, category)
        self.assertEqual(saved_service_2.name, 'xl2tpd')
        self.assertEqual(saved_service_2.category, category)
