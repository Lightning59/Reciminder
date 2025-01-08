import pytest
from django.test import TestCase
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed, assertContains
from users.models import User


@pytest.fixture
def basic_user():
    return User.objects.create_user(username='test', password='kdflsafjiewl')

class TestMainGroup:
    @pytest.mark.django_db
    def test_main_logged_in(self,client, basic_user):
        client.login(username=basic_user.username, password='kdflsafjiewl')
        response = client.get('/')
        assert response.status_code == 200
        assertTemplateUsed(response, 'main.html')
        assertContains(response, 'Logout</a>')


    def test_main_logged_out(self,client):
        response = client.get('/')
        assert response.status_code == 200
        assertTemplateUsed(response, 'main.html')
        assertContains(response, 'Login</a>')


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