import config

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

def test_prod_config():
    assert config.ProdConfig.DEBUG == False
    assert config.ProdConfig.TESTING == False
    assert config.ProdConfig.DATABASE == "real_cert.json"
    assert config.ProdConfig.SECRET_KEY == ""