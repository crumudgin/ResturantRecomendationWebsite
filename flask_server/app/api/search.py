from flask import jsonify
import numpy as np

from . import api
from ..machineLearning.recomendation_model import old_model
from ..db import get_db
from ..models.resturant import Resturant

m = old_model()

@api.route("/search/", methods=["GET"])
def search():
    database = get_db()
    doc = database.collection(u"training_resturants").where(u"zip_code", u"==", 43235)  #TODO swap zipcode for geotag
    resturants = [Resturant.from_dict(i.to_dict()) for i in doc.get()]
    nums = np.array([i.num for i in resturants])
    ratings = m.predict([np.full_like(nums, 569), nums])
    five_star_ratings = []
    for index, rating in enumerate(ratings):
        if max(rating) == rating[4]:
            five_star_resturant = resturants[index]
            five_star_ratings.append({
                "name" : five_star_resturant.name,
                "link" : five_star_resturant.link,
                "address" : five_star_resturant.address,
                "categories" : five_star_resturant.categories,
                "rating" : rating.tolist()
            })

    return jsonify({
        "ratings" : five_star_ratings
    })