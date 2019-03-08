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

def test_dev_config():
    assert config.DevConfig.DEBUG == True
    assert config.DevConfig.TESTING == False
    assert config.DevConfig.DATABASE == "real_cert.json"
    assert config.DevConfig.SECRET_KEY == "dev"

def test_test_config():
    assert config.TestConfig.DEBUG == False
    assert config.TestConfig.TESTING == True
    assert config.TestConfig.DATABASE == "test_cert.json"
    assert config.TestConfig.SECRET_KEY == "dev"