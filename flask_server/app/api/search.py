from flask import jsonify

from . import api
from ..machineLearning.recomendation_model import old_model
from ..machineLearning.recomend import get_recomendations

m = old_model()

@api.route("/search/", methods=["GET"])
def search():
    five_star_ratings = get_recomendations(m, 43235)

    return jsonify({
        "ratings" : five_star_ratings
    })