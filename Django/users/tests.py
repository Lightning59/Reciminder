import pytest
from pytest_django.asserts import assertTemplateUsed, assertRedirects
from django.urls import reverse
from users.test_fixtures_users import *


def test_navigate_to_login_when_logged_out(client):
    """Test going to the login when logged out works and gives the appropriate template"""
    response = client.get(reverse('login'))
    assert response.status_code == 200
    assertTemplateUsed(response, 'login_screen.html')


@pytest.mark.django_db
def test_navigate_to_login_when_logged_in(client, basic_user):
    """A logged-in user that somehow directly requests the login page should just be redirected to the home page"""
    client.force_login(basic_user)
    response = client.get(reverse('login'))
    assertRedirects(response, reverse('home'), status_code=302, target_status_code=200)


def test_navigate_to_logout_when_logged_out(client):
    """A logged-out user that somehow directly requests the logout page should just be redirected to the index landing
     page"""
    response = client.get(reverse('logout'))
    assertRedirects(response, reverse('index'), status_code=302, target_status_code=200)


@pytest.mark.django_db
def test_navigate_to_logout_when_logged_in(client, basic_user):
    """User should be logged out then flipped to index landing page test if user is logged out by trying to go back to
    login page and should get normal login screen (would redirect to home page if user was still logged in)"""
    client.force_login(basic_user)
    response = client.get(reverse('logout'))
    assertRedirects(response, reverse('index'), status_code=302, target_status_code=200)
    response = client.get(reverse('login'))
    assert response.status_code == 200
    assertTemplateUsed(response, 'login_screen.html')


# these try logging in with Post Method
@pytest.mark.django_db
def test_login_with_post(client, basic_user):
    """ Try to log in with right password using post goes to home page"""
    response = client.post(reverse('login'), data={'username': basic_user.username, 'password': 'kdflsafjiewl'})
    assertRedirects(response, reverse('home'), status_code=302, target_status_code=200)


@pytest.mark.django_db
def test_login_with_post_bad_password(client, basic_user):
    """ Try to log in with wrong password using post goes to index page"""
    response = client.post(reverse('login'), data={'username': basic_user.username, 'password': 'notthepassword'})
    assertRedirects(response, reverse('index'), status_code=302, target_status_code=200)


@pytest.mark.django_db
def test_login_with_post_upper_user_name(client, basic_user):
    """ Try to log in with right password using post goes to home page username s/b case-insensitive"""
    response = client.post(reverse('login'), data={'username': basic_user.username.upper(), 'password': 'kdflsafjiewl'})
    assertRedirects(response, reverse('home'), status_code=302, target_status_code=200)


@pytest.mark.django_db
def test_login_with_post_but_with_capslock(client, basic_user):
    """ Try to log in with right password but user left capslock on should still fail to index page"""
    password = 'kdflsafjiewl'
    password = password.upper()
    response = client.post(reverse('login'), data={'username': basic_user.username, 'password': password})
    assertRedirects(response, reverse('index'), status_code=302, target_status_code=200)
