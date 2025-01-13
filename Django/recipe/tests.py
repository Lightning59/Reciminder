import pytest
from pytest_django.asserts import assertRedirects, assertTemplateUsed
import uuid6
from django.test import RequestFactory
from django.urls import reverse
from .views import *
from .models import *
from .forms import *
from users.test_fixtures_users import *


# models
@pytest.fixture
def recipe_with_all_fields():
    return Recipe.objects.create(title='Test Recipe All Fields',
                                 description_free_text='Description of Test Recipe All Fields',
                                 ingredients_free_text='Each and every Field',
                                 instructions_free_text='Process through each field',
                                 servings_per_nominal=2,
                                 original_website_link='www.amazingribs.com')


@pytest.fixture
def recipe_with_only_title():
    return Recipe.objects.create(title='Test Recipe Only Title')


@pytest.mark.django_db
def test_all_fields_str(recipe_with_all_fields):
    assert str(recipe_with_all_fields) == 'Test Recipe All Fields'


@pytest.mark.django_db
def test_only_title_field_str(recipe_with_only_title):
    assert str(recipe_with_only_title) == 'Test Recipe Only Title'


# Test paginate function
@pytest.fixture
def list_of_ten_strings():
    return ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']


@pytest.fixture
def http_request_no_page():
    request_factory = RequestFactory()
    request = request_factory.get('/home')
    return request


@pytest.fixture
def http_request_page2():
    request_factory = RequestFactory()
    request = request_factory.get('/home/?page=2')
    return request


@pytest.fixture
def http_request_page4():
    request_factory = RequestFactory()
    request = request_factory.get('/home/?page=4')
    return request


@pytest.fixture
def http_request_page5():
    request_factory = RequestFactory()
    request = request_factory.get('/home/?page=5')
    return request


# No page attribute: List of 10 items, items per page 3, should return list of first 3 items, 4
def test_paginate_ten_take3_no_page(http_request_no_page, list_of_ten_strings):
    queryset, total_pages = paginate_recipes(http_request_no_page, list_of_ten_strings, 3)
    assert queryset.object_list == ['a', 'b', 'c']
    assert total_pages == 4


# no page attribute: list of 10 items, itemps per page 10, should return all10, 1
def test_paginate_ten_take10_no_page(http_request_no_page, list_of_ten_strings):
    queryset, total_pages = paginate_recipes(http_request_no_page, list_of_ten_strings, 10)
    assert queryset.object_list == ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    assert total_pages == 1


# no page attribute: list of 10 items, itemps per page 20, should return all10, 1
def test_paginate_ten_take20_no_page(http_request_no_page, list_of_ten_strings):
    queryset, total_pages = paginate_recipes(http_request_no_page, list_of_ten_strings, 20)
    assert queryset.object_list == ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    assert total_pages == 1


# page=2: List of 10 items, items per page 3, should return list of next 3 items, 4
def test_paginate_ten_take3_page2(http_request_page2, list_of_ten_strings):
    queryset, total_pages = paginate_recipes(http_request_page2, list_of_ten_strings, 3)
    assert queryset.object_list == ['d', 'e', 'f']
    assert total_pages == 4


# page=4: List of 10 items, items per page 3, should return last item, 4
def test_paginate_ten_take3_page4(http_request_page4, list_of_ten_strings):
    queryset, total_pages = paginate_recipes(http_request_page4, list_of_ten_strings, 3)
    assert queryset.object_list == ['j']
    assert total_pages == 4


# page=5: List of 10 items, items per page 3, should return last item, 4
def test_paginate_ten_take3_page5(http_request_page5, list_of_ten_strings):
    queryset, total_pages = paginate_recipes(http_request_page5, list_of_ten_strings, 3)
    assert queryset.object_list == ['j']
    assert total_pages == 4


# Test search function somehow.
class TestRecipeSearch:
    @pytest.fixture
    def recipe_search_group(self):
        recipe1 = Recipe.objects.create(title='cat',
                                        description_free_text='cat',
                                        ingredients_free_text='cat',
                                        instructions_free_text='cat',
                                        original_website_link='www.cat.com')
        recipe2 = Recipe.objects.create(title='dogcat',
                                        description_free_text='cat',
                                        ingredients_free_text='cat',
                                        instructions_free_text='cat',
                                        original_website_link='www.fox.com')
        recipe3 = Recipe.objects.create(title='cat 2',
                                        description_free_text='dog',
                                        ingredients_free_text='cat',
                                        instructions_free_text='cat',
                                        original_website_link='www.fox.com')
        recipe4 = Recipe.objects.create(title='cat 3',
                                        description_free_text='cat',
                                        ingredients_free_text='dog',
                                        instructions_free_text='cat',
                                        original_website_link='www.cat.com')
        recipe5 = Recipe.objects.create(title='cat 4',
                                        description_free_text='cat',
                                        ingredients_free_text='cat',
                                        instructions_free_text='dog',
                                        original_website_link='www.bird.com')
        recipe6 = Recipe.objects.create(title='cat 5',
                                        description_free_text='cat',
                                        ingredients_free_text='cat',
                                        instructions_free_text='cat',
                                        original_website_link='www.dog.com')
        recipe7 = Recipe.objects.create(title='cat 6',
                                        description_free_text='cat',
                                        ingredients_free_text='elephant',
                                        instructions_free_text='fox',
                                        original_website_link='www.dog.com',
                                        deleted_by_user=True)

    @pytest.fixture
    def search_query_none(self):
        rf = RequestFactory()
        request = rf.get('/')
        return request

    @pytest.fixture
    def search_query_bird(self):
        rf = RequestFactory()
        request = rf.get('/?search_query=bird')
        return request

    @pytest.fixture
    def search_query_dog(self):
        rf = RequestFactory()
        request = rf.get('/?search_query=dog')
        return request

    @pytest.fixture
    def search_query_elephant(self):
        rf = RequestFactory()
        request = rf.get('/?search_query=elephant')
        return request

    @pytest.fixture
    def search_query_fox(self):
        rf = RequestFactory()
        request = rf.get('/?search_query=fox')
        return request

    # search with no query should match all but the deleted item
    @pytest.mark.django_db
    def test_search_no_search(self, recipe_search_group, search_query_none):
        recipes_found, query_term = search_recipes(search_query_none)
        assert query_term == ''
        assert recipes_found.count() == 6

    # search a term that only matches one of them should only get that one
    @pytest.mark.django_db
    def test_search_bird(self, recipe_search_group, search_query_bird):
        recipes_found, query_term = search_recipes(search_query_bird)
        assert query_term == 'bird'
        assert recipes_found.count() == 1

    # search a term that matches all but one each in a different field should get all but that one
    @pytest.mark.django_db
    def test_search_dog(self, recipe_search_group, search_query_dog):
        recipes_found, query_term = search_recipes(search_query_dog)
        assert query_term == 'dog'
        assert recipes_found.count() == 5

    # search a term that matches none (or only deleted items) should get none
    @pytest.mark.django_db
    def test_search_elephant(self, recipe_search_group, search_query_elephant):
        recipes_found, query_term = search_recipes(search_query_elephant)
        assert query_term == 'elephant'
        assert recipes_found.count() == 0

    # search a term that matches 2 should get those 2
    @pytest.mark.django_db
    def test_search_fox(self, recipe_search_group, search_query_fox):
        recipes_found, query_term = search_recipes(search_query_fox)
        assert query_term == 'fox'
        assert recipes_found.count() == 2


# forms
# try to submit a form with all fields proper
def test_form_all_field_ok():
    form_data = {
        'title': 'Good Food Recipe!',
        'description_free_text': 'This is just a great recipe',
        'ingredients_free_text': 'Good ingredient 1 \n Good ingredient 2 \n Good ingredient 3',
        'instructions_free_text': 'Do this \n Then do this \n then do this.',
        'servings_per_nominal': 4
    }
    form = RecipeForm(data=form_data)
    assert form.is_valid()

# Try to sumit a form with only title
def test_form_only_title():
    form_data = {
        'title': 'Good Food Recipe! But Lazy.',
    }
    form = RecipeForm(data=form_data)
    assert form.is_valid()

# try to submit blank
def test_form_all_field_blank():
    form_data = {
        'title': '',
        'description_free_text': '',
        'ingredients_free_text': '',
        'instructions_free_text': ''
    }
    form = RecipeForm(data=form_data)
    assert not form.is_valid()

# try to submit all fields except title
def test_form_all_but_title():
    form_data = {
        'title': '',
        'description_free_text': 'This is just a great recipe',
        'ingredients_free_text': 'Good ingredient 1 \n Good ingredient 2 \n Good ingredient 3',
        'instructions_free_text': 'Do this \n Then do this \n then do this.',
        'servings_per_nominal': '4'
    }
    form = RecipeForm(data=form_data)
    assert not form.is_valid()

# try to submit non-numeric to numeric.
def test_form_all_good_but_bad_number():
    form_data = {
        'title': 'Good Food Recipe!',
        'description_free_text': 'This is just a great recipe',
        'ingredients_free_text': 'Good ingredient 1 \n Good ingredient 2 \n Good ingredient 3',
        'instructions_free_text': 'Do this \n Then do this \n then do this.',
        'servings_per_nominal': 'seven'
    }
    form = RecipeForm(data=form_data)
    assert not form.is_valid()
# Try float vs decimal
def test_form_all_field_ok_float():
    form_data = {
        'title': 'Good Food Recipe!',
        'description_free_text': 'This is just a great recipe',
        'ingredients_free_text': 'Good ingredient 1 \n Good ingredient 2 \n Good ingredient 3',
        'instructions_free_text': 'Do this \n Then do this \n then do this.',
        'servings_per_nominal': '3.5'
    }
    form = RecipeForm(data=form_data)
    assert form.is_valid()
# Try a negative number
def test_form_all_field_no_negatives():
    form_data = {
        'title': 'Good Food Recipe!',
        'description_free_text': 'This is just a great recipe',
        'ingredients_free_text': 'Good ingredient 1 \n Good ingredient 2 \n Good ingredient 3',
        'instructions_free_text': 'Do this \n Then do this \n then do this.',
        'servings_per_nominal': '-3'
    }
    form = RecipeForm(data=form_data)
    assert not form.is_valid()

# views
@pytest.fixture
def recipe_scrub_search_group():
    recipe1 = Recipe.objects.create(title='cat',
                                        description_free_text='cat',
                                        ingredients_free_text='cat',
                                        instructions_free_text='cat',
                                        original_website_link='www.cat.com')

    recipe2 = Recipe.objects.create(title='cat 6',
                                        description_free_text='cat',
                                        ingredients_free_text='elephant',
                                        instructions_free_text='fox',
                                        original_website_link='www.dog.com',
                                        deleted_by_user=True)

@pytest.fixture
def random_current_uuid():
    return uuid6.uuid7()


# have a db with a valid recipe, deleted recipe, Then also generate a valid UUID at random
# Scrub function should return a recipe object, Raise Error, Raise Error respectively
@pytest.mark.django_db
def test_scrub_vaild_recipe(recipe_scrub_search_group):
    valid_recipe=Recipe.objects.get(title='cat')
    valid_key=valid_recipe.pk
    recipe=Recipe.objects.get(title='cat')
    srubbed_recipe = scrub_invalid_recipe_pk(valid_key)
    assert recipe == srubbed_recipe


@pytest.mark.django_db
def test_scrub_vaild_recipe_deleted(recipe_scrub_search_group):
    test_recipe=Recipe.objects.get(title='cat 6')
    test_key=test_recipe.pk
    exmessage=''
    extype=None
    try:
        scrub_invalid_recipe_pk(test_key)
    except Exception as e:
        extype = type(e)
        exmessage = str(e)
    assert exmessage == "Recipe was deleted"
    assert extype is Http404


@pytest.mark.django_db
def test_scrub_vaild_recipe_randomuuid(recipe_scrub_search_group,random_current_uuid):
    test_key=random_current_uuid
    test_recipe=str(test_key)
    exmessage=''
    extype=None
    try:
        scrub_invalid_recipe_pk(test_recipe)
    except Exception as e:
        extype = type(e)
        exmessage = str(e)
    assert exmessage == "Recipe does not exist"
    assert extype is Http404


# attempt to access add-recipe while logged out
def test_add_recipe_while_logged_out(client):
    response = client.get(reverse('add-recipe'))
    assertRedirects(response,reverse('login')+'?next=/recipe/addrecipe/', status_code=302, target_status_code=200)

# attempt to access add-recipe while logged in
@pytest.mark.django_db
def test_add_recipe_when_logged_in(client, basic_user):
    client.force_login(basic_user)
    response = client.get(reverse('add-recipe'))
    assert response.status_code == 200
    assertTemplateUsed(response, 'add-recipe.html')

# attempt to post a valid form
@pytest.mark.django_db
def test_post_recipe(client, basic_user):
    client.force_login(basic_user)
    response = client.post(reverse('add-recipe'), data={'title': 'Good Recipe',
                                                        'description_free_text': 'This recipe is good'})
    assertRedirects(response, reverse('home'), status_code=302, target_status_code=200)
    num_recipes = Recipe.objects.count()
    assert num_recipes == 1

# attempt to post an invalid form
@pytest.mark.django_db
def test_post_recipe_no_title(client, basic_user):
    client.force_login(basic_user)
    response = client.post(reverse('add-recipe'), data={'title': '',
                                                        'description_free_text': 'This recipe is good'})
    assert response.status_code == 200
    assertTemplateUsed(response, 'add-recipe.html')
    num_recipes = Recipe.objects.count()
    assert num_recipes == 0

# attempt to access view-recipe while logged out valid recipe
# attempt to access view-recipe while logged in valid recipe


# attempt to delete recip while logged out invalid recipe
# attempt to delete recipe while logged in invalid recipe

# attempt to access edit recipe while logged out valid recipe
# attempt to access edit recipe while logged in valid recipe
# attempt to access recipe while logged out invalid recipe
# attempt to access recipe while logged in invalid recipe
# attempt to post update to recipe while logged in valid recipe
# attempt to post update to recipe while logged out valid recipe
# attempt to post update to recipe blank title while logged out valid recipe
# attempt to post update to recipe blank title while logged in valid recipe

# attempt to delete recipe while logged out valid recipe
# attempt to delete recipe while logged in valid recipe
# attempt to delete recipe while logged out invalid recipe
# attempt to delete recipe while logged in invalid recipe

# attempt to view home logged in
# attempt to view home logged out
