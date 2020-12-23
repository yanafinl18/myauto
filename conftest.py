import pytest
import data.users as users
from fixtures.auth_fixture import session

@pytest.fixture(scope="session")
def test_user():
    """ Создание фикстуры test_user с уровнем сессия, в ответе передаются данные по клиенту"""

    print("user is created")
    user = users.reimond
    return user


