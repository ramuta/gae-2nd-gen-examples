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


def test_profile_main(client):
    user = User.get_by_username(username="testman")
    assert user is not None

    response = client.get('/profile')

    assert b'My profile' in response.data
    assert b'Delete' in response.data  # if there's at least one session on the list, there's also a Delete button
    # check if session token hash (first five chars) is in the sessions list (as session ID)
    assert str.encode("{}".format(user.sessions[0].token_hash[:5])) in response.data
