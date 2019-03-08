from flask import jsonify

from . import api

@api.route("/endpoint/", methods=["GET"])
def hello():
    return jsonify({
        "Hello" : "World!"
    })