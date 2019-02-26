import os
import tempfile
import hashlib

import pytest

from flask import g, current_app
from flaskr import create_app
from flaskr.db import get_db, init_db
from flaskr.models.resturant import Resturant
from firebase_admin import firestore

@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'DATABASE': "C:/Users/zacch/Documents/GitHub/ResturantRecomendationWebsite/test_cert.json",
    })

    yield app

@pytest.fixture
def client(app):
    return app.test_client()


def test_index(client):
    """ Test that the server works at the most basic of levels """
    response = client.get("/")
    assert response.status_code == 200
    assert response.data == b'Hello, World!'


def test_database(client):
    """ Test that the database connects"""
    assert isinstance(get_db(), type(firestore.client()))


@pytest.mark.parametrize(("address",                 "categories",                      "finished", "link",       "name",      "num", "state", "zip_code"),
                        [("1234 test St. OH, 43235", {"0" : "a", "1" : "b", "2" : "c"}, True,       "/test/link", "resturant",  1234, "OH",    7760),  # Test basic resturant creation
                         ("test",                    {"0" : "a", "1" : "b"},            True,       "test",       "test",       1,    "TEST",  1)      # Test that the resturant creation works dynamicaly
                        ])
def test_resturant_creation(client, address, categories, finished, link, name, num, state, zip_code):
    resturant = Resturant(address, categories, finished, link, name, num, state, zip_code)
    resturant_from_dict = Resturant.from_dict(resturant.to_dict())
    assert resturant.hashed_name == hashlib.sha224(resturant.name.encode("utf-8")).hexdigest()
    assert resturant_from_dict == resturant

