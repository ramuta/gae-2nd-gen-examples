from urllib.request import Request, urlopen

import pytest

from main import app
from models.user import User


@pytest.fixture
def client():
    client = app.test_client()

    cleanup()  # clean up before every test

    yield client


def cleanup():
    # clean up/delete the database (reset Datastore)
    urlopen(Request("http://localhost:8002/reset", data={}))  # this sends an empty POST request


def test_generate_session_token(client):
    # create User model and log it in
    user = User.create(username="testman", password="test123")
    session_token = User.generate_session_token(user=user)
    client.set_cookie(server_name="localhost", key="my-web-app-session", value=session_token)

    assert user.sessions != []


def test_find_user_by_session_token(client):
    # create User model and log it in
    user = User.create(username="testman", password="test123")
    session_token = User.generate_session_token(user=user)
    client.set_cookie(server_name="localhost", key="my-web-app-session", value=session_token)

    assert user.sessions != []

    find_user = User.get_by_session_token(session_token=session_token)
    assert find_user is not None
