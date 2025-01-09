import pytest
from users.models import User


@pytest.fixture
def basic_user():
    return User.objects.create_user(username='test', password='kdflsafjiewl')
