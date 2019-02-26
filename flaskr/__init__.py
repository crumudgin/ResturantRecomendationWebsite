import os

from flask import Flask
from flaskr.db import init_db, get_db
from flaskr.machine_learning.recomendation_model import *
from flaskr.endpoints.index import index
from flaskr.endpoints.search import search
from flask_api import FlaskAPI

def create_app(test_config=None):

    app =  FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE="real_cert.json",
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    with app.app_context():
        try:
            init_db()
        except:
            print("I'm doing it again")
    print("ready and waiting")

    # a simple page that says hello
    @app.route('/', methods=['GET'])
    def hello_endpoint():
        return index()

    @app.route('/search/', methods=['GET'])
    def search_endpoint():
        db = get_db()
        doc = db.collection(u"training_resturants")
        resturants = doc.where(u"zip_code", u"==", 43235).get()
        m = old_model()
        m._make_predict_function()
        return search(m, resturants)

    return app