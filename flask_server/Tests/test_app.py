import os
import tempfile
import hashlib
from unittest import mock

import pytest

from app import create_app
import config


@pytest.fixture
def app():
    app = create_app("test.cfg")

    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_configs():
    assert config.DevConfig.DEBUG == True
    assert config.DevConfig.TESTING == False
    assert config.DevConfig.DATABASE == "real_cert.json"
    assert config.DevConfig.SECRET_KEY == "dev"