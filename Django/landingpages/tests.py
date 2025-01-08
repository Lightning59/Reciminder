import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed, assertContains
from users.models import User


@pytest.fixture
def basic_user():
    return User.objects.create_user(username='test', password='kdflsafjiewl')


class TestMainGroup:
    """Tests for the main.html template using the index landing page
    Mainly tests for if the header displaying something reasonable"""

    @pytest.mark.django_db
    def test_main_logged_in(self, client, basic_user):
        client.login(username=basic_user.username, password='kdflsafjiewl')
        response = client.get('/')
        assert response.status_code == 200
        assertTemplateUsed(response, 'main.html')
        assertContains(response, 'Logout</a>')

    def test_main_logged_out(self, client):
        response = client.get('/')
        assert response.status_code == 200
        assertTemplateUsed(response, 'main.html')
        assertContains(response, 'Login</a>')


class TestLandingPageView:
    """tests that the index landing page is being served correctly Likely needs update once page is matured"""

    def test_call_index_directly(self, client):
        response = client.get('/')
        assert response.status_code == 200
        assertTemplateUsed(response, 'landing_page.html')
        assertContains(response, 'Project is still in work.</p>')

    def test_call_index_by_reverse(self, client):
        response = client.get(reverse('index'))
        assert response.status_code == 200
        assertTemplateUsed(response, 'landing_page.html')
        assertContains(response, 'Project is still in work.</p>')
