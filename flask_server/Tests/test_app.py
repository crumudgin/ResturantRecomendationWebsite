import hashlib
import json

import pytest
from firebase_admin import firestore

from app import create_app, m
from app.db import get_db
from app.models.resturant import Resturant
from app.models.user import User
import config


@pytest.fixture
def app():
    app = create_app(config.TestConfig)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_api_search(client):
    response = client.get("/api/v1/search/")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data["ratings"], list)

def test_database(app):
    """ Test that the database connects"""
    assert isinstance(get_db(), type(firestore.client()))


@pytest.mark.parametrize(("address",                 "categories",                      "finished", "link",       "name",      "num", "state", "zip_code"),
                        [("1234 test St. OH, 43235", {"0" : "a", "1" : "b", "2" : "c"}, True,       "/test/link", "resturant",  1234, "OH",    7760),  # Test basic resturant creation
                         ("test",                    {"0" : "a", "1" : "b"},            False,      "test",       "test",       1,    "TEST",  1)      # Test that the resturant creation works dynamicaly
                        ])
def test_resturant_creation(client, address, categories, finished, link, name, num, state, zip_code):
    resturant = Resturant(address, categories, finished, link, name, num, state, zip_code)
    resturant_from_dict = Resturant.from_dict(resturant.to_dict())
    assert resturant.hashed_name == hashlib.sha224(resturant.name.encode("utf-8")).hexdigest()
    assert resturant_from_dict == resturant
    assert resturant != 5

@pytest.mark.parametrize(("num", "name",   "email", "password"),
                        [(1,     "test",   "test", "test"),
                         (2,     "second", "email", "password")
                        ])
def test_user_creation(num, name, email, password):
    user = User(num, name, email, password)
    assert user.num == num
    assert user.name == name
    assert user.email == email
    assert user == User.from_dict(user.to_dict())
    assert user != User(-1, "not the user", "", "")
    assert user != 5
    