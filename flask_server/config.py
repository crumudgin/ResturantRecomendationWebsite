class DevConfig():
    DEBUG = True
    TESTING = False
    DATABASE = "real_cert.json"
    SECRET_KEY = "dev"

class TestConfig():
    DEBUG = False
    TESTING = True
    DATABASE = "test_cert.json"
    SECRET_KEY = "dev"

