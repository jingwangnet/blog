from django.test import TestCase
from django.urls import resolve
from .views import home_page

# Create your tests here.
class HomePageTest(TestCase):
    
    def test_can_resolve_root_url_to_home_page(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)
