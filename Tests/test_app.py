import os
import tempfile
import hashlib

import pytest

from flask import g, current_app
from flaskr import create_app
from flaskr.db import get_db, init_db
from flaskr.models.resturant import Resturant

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
    response = client.get("/")
    assert response.status_code == 200
    assert response.data == b'Hello, World!'


@pytest.mark.parametrize(("address",                 "categories",    "finished", "link",       "name",      "num", "state", "zip_code"),
                        [("1234 test St. OH, 43235", {"0" : "a", "1" : "b", "2" : "c"}, True,       "/test/link", "resturant", 1234,  "OH",    7760)])
def test_resturants(client, address, categories, finished, link, name, num, state, zip_code):
    db = get_db().collection(u"training_resturants")
    resturant = Resturant(address, categories, finished, link, name, num, state, zip_code)
    doc = db.document(resturant.hashed_name)
    doc.set(resturant.to_dict())
    resturant_from_db = Resturant.from_dict(doc.get().to_dict())
    assert resturant.hashed_name == hashlib.sha224(resturant.name.encode("utf-8")).hexdigest()
    assert resturant_from_db == resturant
    doc.delete()

