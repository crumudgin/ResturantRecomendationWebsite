import requests
from config import DevConfig
from app import create_app
from flask import Flask
from app.db import get_db
from app.models.resturant import Resturant

app = create_app(DevConfig)
app.run(host="0.0.0.0", port=5000, debug=True)

@app.cli.command()
def geolocate():
    database = get_db()
    doc = database.collection(u"training_resturants").order_by(u"num")
    query = list(doc.limit(1000).get())
    counter = len(query)
    while counter > 1:
        for i in query:
            resturant = Resturant.from_dict(i.to_dict())
            if resturant.latitude is not None:
                continue
            url = "https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s" %(resturant.web_safe_address(), app.config["SECRET_KEY"])
            print(url)
            response = requests.get(url)
            try:
                latitude = response.json()["results"][0]["geometry"]["location"]["lat"]
                longitude = response.json()["results"][0]["geometry"]["location"]["lng"]
                resturant.latitude = latitude
                resturant.longitude = longitude
                database.collection(u"training_resturants").document(resturant.hashed_name).set(resturant.to_dict())
            except:
                print(resturant.num)
        query = list(doc.start_after({u"num" : resturant.num}).limit(1000).get())
        counter = len(query)