import os

import numpy as np

from flask import Flask
from flaskr.db import init_db, get_db
from flaskr.machine_learning.recomendation_model import *

def recomend_based_on_zip(model, zip_codes, user_num):
	resturants, nums = resturants_from_zip(zip_codes)
	links = [i["link"] for i in resturants]
	nums = np.array(nums)
	ratings = model.predict([np.full_like(nums, user_num), nums])
	# ratings, links = sort_lists(ratings, links)
	for index, rating in enumerate(ratings):
		highest = rating[0]
		highest_index = 0
		for rating_index, i in enumerate(rating):
			if i > highest:
				highest = i
				highest_index = rating_index

def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)
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
            pass
    m = old_model()
    print("ready and waiting")

    # a simple page that says hello
    @app.route('/')
    def hello():
        db = get_db()
        doc = db.collection(u"training_resturants")
        resturants = doc.where(u"zip_code", u"==", 43235).get()
        nums = [i.to_dict()["num"] for i  in resturants]
        nums = np.array(nums)
        ratings = m.predict([np.full_like(nums, 569), nums])
        # for i, rating in enumerate(ratings):
        #     print(rating)
        return 'Hello, World!'

    return app
