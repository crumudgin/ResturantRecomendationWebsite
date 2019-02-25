import os
import tempfile

import pytest

from flaskr import create_app
from flaskr.db import get_db, init_db

@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'DATABASE': "test_cert.json",
    })

    with app.app_context():
        init_db()

    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.data == b'Hello, World!'