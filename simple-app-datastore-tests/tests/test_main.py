from urllib.request import urlopen, Request

import pytest
from main import app


@pytest.fixture
def client():
    client = app.test_client()

    cleanup()  # clean up before every test

    yield client


def cleanup():
    # clean up/delete the database (reset Datastore)
    urlopen(Request("http://localhost:8002/reset", data={}))  # this sends an empty POST request


def test_index_page(client):
    response = client.get('/')
    assert b'Enter your message' in response.data


def test_basic_page(client):
    response = client.get('/basic')
    assert b'Basic handler without HTML template' in response.data


def test_index_page_create_message(client):
    response = client.post('/', data={"message": "I am testing"})

    assert b'Enter your message' in response.data
    assert b"I am testing" in response.data
