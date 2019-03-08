from flask import Flask

def create_app(environment):
    
    app = Flask(__name__)

    with open(environment) as env:
        app.config.from_envvar(env)
    return app