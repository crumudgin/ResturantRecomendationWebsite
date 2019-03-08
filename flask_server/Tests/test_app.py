import hashlib
import json

import pytest
from firebase_admin import firestore

from app import create_app
from app.db import get_db
from app.models.resturant import Resturant
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


@pytest.mark.parametrize(("address",                 "categories",                      "finished", "link",       "name",      "num", "state", "zip_code"),
                        [("1234 test St. OH, 43235", {"0" : "a", "1" : "b", "2" : "c"}, True,       "/test/link", "resturant",  1234, "OH",    7760),  # Test basic resturant creation
                        ])
def test_resturant_creation(client, address, categories, finished, link, name, num, state, zip_code):
    resturant = Resturant(address, categories, finished, link, name, num, state, zip_code)
    resturant_from_dict = Resturant.from_dict(resturant.to_dict())
    assert resturant.hashed_name == hashlib.sha224(resturant.name.encode("utf-8")).hexdigest()
    assert resturant_from_dict == resturant