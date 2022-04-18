from django.test import TestCase
from django.http import HttpRequest
from django.urls import resolve
from .views import home_page

# Create your tests here.
class HomePageTest(TestCase):
    
    def test_use_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


