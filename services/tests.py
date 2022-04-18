from django.test import TestCase
from django.http import HttpRequest
from django.urls import resolve
from .views import home_page

# Create your tests here.
class HomePageTest(TestCase):
    
    def test_can_resolve_root_url_to_home_page(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_return_correct_html(self):
        request = HttpRequest()
        response = home_page(request)

        html = response.content.decode()

        self.assertTrue(html.startswith('<html>'))
        self.assertIn('<title>静网</title>', html)
        self.assertTrue(html.endswith('</html>'))


