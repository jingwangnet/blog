from django.test import TestCase
from django.http import HttpRequest
from django.urls import resolve
from .views import home_page
from .models import Service

# Create your tests here.
class HomePageTest(TestCase):
    
    def test_use_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


    def test_can_save_a_post_request(self):
        data = {
            'new_service': 'A service'
        }
        response = self.client.post('/', data=data)
     
        self.assertEqual(1, Service.objects.count())
        service = Service.objects.first()
        self.assertEqual(service.name, 'A service')

        html = response.content.decode()
        self.assertIn('A service', html)
        self.assertTemplateUsed(response, 'home.html')


class ServiceModelTest(TestCase):

    def test_creating_and_saving_service(self):
        service_1 = Service()
        service_1.name = 'pptpd'
        service_1.save()
        service_2 = Service()
        service_2.name = 'xl2tpd'
        service_2.save()

        self.assertEqual(2, Service.objects.count())

        saved_service_1, saved_service_2 = Service.objects.all()

        self.assertEqual(saved_service_1.name, 'pptpd')
        self.assertEqual(saved_service_2.name, 'xl2tpd')
