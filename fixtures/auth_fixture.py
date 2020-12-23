import pytest
from helpers.auth_helpers import Session


@pytest.fixture(scope="session")
def session(test_user):
    """ Создание фикстуры session с уровнем сессия. В качестве атрибута тут передана функция test_user

    Parameters
    ----------
    - test_user

    На выходе получаем сгенерированный SessionToken для пользователя test_user , используя класс Session"""

    session = Session(test_user)
    session.create_session()
    return session



