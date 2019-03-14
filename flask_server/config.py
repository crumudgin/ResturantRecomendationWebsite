import os

def try_to_get_env(key, default=""):
    try:
        return os.environ[key]
    except:
        return default

class BaseConfig():
    DEBUG = False
    TESTING = False
    DATABASE = "real_cert.json"
    SECRET_KEY = "dev"
    ROUTE_KEY = try_to_get_env("ROUTE_KEY", "")

class DevConfig(BaseConfig):
    DEBUG = True

class TestConfig(BaseConfig):
    TESTING = True
    DATABASE = "test_cert.json"

class ProdConfig(BaseConfig):
    SECRET_KEY = try_to_get_env("SECRET_KEY", "")




