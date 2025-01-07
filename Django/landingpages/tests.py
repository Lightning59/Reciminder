from django.test import TestCase
from django.urls import reverse



class LandingPageViewTests(TestCase):
    def test_call_index_directly(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'landing_page.html')
        self.assertContains(response, 'Project is still in work.</p>')

    def test_call_index_by_reverse(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'landing_page.html')
        self.assertContains(response, 'Project is still in work.</p>')