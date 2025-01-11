import pytest
from django.test import RequestFactory
from .views import *
from .models import *
from .forms import *


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
    assert queryset.object_list == ['a','b', 'c']
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
# Get a database with ~5-10 items loaded
# search a term that only matches one of them should only get that one
# search a term that matches all but one each in a different field should get all but that one
# search a term that matches none should get none
# search a term that matches 2 should get those 2

# forms
# try to submit a form with all fields proper
# Try to sumit a form with only title
# try to submit blank
# try to submit all fields except title
# try to submit non-numeric to numeric.
# Try float vs decimal
# Try a negative number

# views
# have a db with a valid recipe, deleted recipe, Then also generate a valid UUID at random
# Scrub function should return a recipe object, Raise Error, Raise Error respectively

# attempt to access add-recipe while logged out
# attemp to access add-recipe while logged in
# attempt to post a valid form
# attempt to post an invalid form

# attempt to access view-recipe while logged out valid recipe
# attemp to access view-recipe while logged in valid recipe
# attempt to delete recip while logged out invalid recipe
# attemp to delete recipe while logged in invalid recipe

# attempt to access edit recipe while logged out valid recipe
# attempt to access edit recipe while logged in valid recipe
# attempt to access recipe while logged out invalid recipe
# attempt to access recipe while logged in invalid recipe
# attempt to post update to recipe while logged in valid recipe
# attempt to post update to recipe while logged out valid recipe
# attempt to post update to recipe blank title while logged out valid recipe
# attempt to post update to recipe blank title while logged in valid recipe

# attempt to delete recipe while logged out valid recipe
# attemp to delete recipe while logged in valid recipe
# attempt to delete recipe while logged out invalid recipe
# attemp to delete recipe while logged in invalid recipe

# attempt to view home logged in
# attempt to view home logged out
