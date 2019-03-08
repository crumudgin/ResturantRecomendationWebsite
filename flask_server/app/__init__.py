from flask import Flask

from .api import api as api_blueprint

def create_app(config):
    
    app = Flask(__name__)

    app.config.from_object(config)

    app.register_blueprint(api_blueprint, url_prefix="/api/v1")

    return app