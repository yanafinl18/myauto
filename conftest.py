import pytest
import data.users as users

@pytest.fixture(scope="session")
def test_user():
    print("user is created")
    user = users.reimond
    return user


