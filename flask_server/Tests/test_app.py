import os
import tempfile
import hashlib
import json
from unittest import mock

import pytest
from firebase_admin import firestore

from app import create_app
from app.db import get_db
import config


@pytest.fixture
def app():
    app = create_app(config.TestConfig)

    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_api_endpoint(client):
    response = client.get("/api/v1/endpoint/")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data == {
        "Hello" : "World!"
    }

def test_database(app):
    """ Test that the database connects"""
    assert isinstance(get_db(), type(firestore.client()))

