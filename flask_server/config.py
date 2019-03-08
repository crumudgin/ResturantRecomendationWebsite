class BaseConfig():
    DEBUG = False
    TESTING = False
    DATABASE = "real_cert.json"
    SECRET_KEY = "dev"

class DevConfig(BaseConfig):
    DEBUG = True

class TestConfig(BaseConfig):
    TESTING = True
    DATABASE = "test_cert.json"

class ProdConfig(BaseConfig):
    SECRET_KEY = ""

