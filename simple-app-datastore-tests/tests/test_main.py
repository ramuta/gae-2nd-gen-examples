import os
import pytest
from main import app


@pytest.fixture
def client():
    os.environ["TESTING"] = "yes"

    client = app.test_client()

    cleanup()  # clean up before every test

    yield client


def cleanup():
    # clean up/delete the DB (drop all tables in the database)
    pass


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
