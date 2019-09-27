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


def test_test_page(client):
    response = client.get('/test')
    assert b'test' in response.data
