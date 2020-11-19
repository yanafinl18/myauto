import pytest
from helpers.auth_helpers import Session


@pytest.fixture(scope="session")
def session(test_user):
    session = Session(test_user)
    session.create_session()
    return session



