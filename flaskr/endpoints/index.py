import numpy as np
from keras import backend as K
from flaskr.db import init_db, get_db



def index():
    return {"hello": "world"}