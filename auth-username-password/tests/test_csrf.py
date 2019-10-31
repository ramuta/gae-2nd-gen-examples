from urllib.request import Request, urlopen

import pytest

from main import app
from models.user import User


@pytest.fixture
def client():
    client = app.test_client()

    cleanup()  # clean up before every test

    # create User model and log it in
    # login is required for all handlers in this file
    user = User.create(username="testman", password="test123")
    session_token = User.generate_session_token(user=user)
    client.set_cookie(server_name="localhost", key="my-web-app-session", value=session_token)

    yield client


def cleanup():
    # clean up/delete the database (reset Datastore)
    urlopen(Request("http://localhost:8002/reset", data={}))  # this sends an empty POST request


def test_set_csrf_token_1(client):
    """Create a CSRF token and make sure the list of CSRF tokens in the User object is not empty."""
    user = User.get_by_username(username="testman")
    assert user is not None

    User.set_csrf_token(user)
    assert user.csrf_tokens != []


def test_set_csrf_token_2(client):
    """create 5 csrf tokens and make sure the list length is 5"""
    user = User.get_by_username(username="testman")
    assert user is not None

    User.set_csrf_token(user)
    User.set_csrf_token(user)
    User.set_csrf_token(user)
    User.set_csrf_token(user)
    User.set_csrf_token(user)

    assert user.csrf_tokens != []
    assert len(user.csrf_tokens) == 5


def test_set_csrf_token_3(client):
    """create 11 csrf tokens and make sure the first one is not in the list anymore (max is 10)"""
    user = User.get_by_username(username="testman")
    assert user is not None

    oldest_token = User.set_csrf_token(user)

    # 10 tokens:
    User.set_csrf_token(user)
    User.set_csrf_token(user)
    User.set_csrf_token(user)
    User.set_csrf_token(user)
    User.set_csrf_token(user)
    User.set_csrf_token(user)
    User.set_csrf_token(user)
    User.set_csrf_token(user)
    User.set_csrf_token(user)
    youngest_token = User.set_csrf_token(user)

    assert user.csrf_tokens != []
    assert len(user.csrf_tokens) == 10

    # assert that the oldest token is not in the csrf tokens list anymore
    assert next((x for x in user.csrf_tokens if x.token == oldest_token), None) is None

    # assert that the youngest created token is still in the csrf list
    assert next((x for x in user.csrf_tokens if x.token == youngest_token), None) is not None


def test_validate_csrf_token(client):
    # create a user
    user = User.get_by_username(username="testman")
    assert user is not None

    # create a CSRF token
    token = User.set_csrf_token(user)
    assert user.csrf_tokens != []

    # validate the token
    assert User.is_csrf_token_valid(user=user, csrf_token=token) is True
