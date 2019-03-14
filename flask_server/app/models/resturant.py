import hashlib

class Resturant:

    def __init__(self, address, categories, finished, link, name, num, state=None, zip_code=None, latitude=None, longitude=None):
            self.hashed_name = hashlib.sha224(name.encode("utf-8")).hexdigest()
            self.address = address
            self.categories = categories
            self.finished = finished
            self.link = link
            self.name = name
            self.num = num
            self.state = state
            self.zip_code = zip_code
            self.latitude = latitude
            self.longitude = longitude

    @staticmethod
    def from_dict(resturant):
        params = [
            resturant["address"], 
            resturant["categories"], 
            resturant["finished"], 
            resturant["link"], 
            resturant["name"], 
            resturant["num"]
            ]
        if "state" in resturant and "zip_code" in resturant:
            params.append(resturant["state"])
            params.append(resturant["zip_code"])

        if "latitude" in resturant and "longitude" in resturant:
            params.append(resturant["latitude"])
            params.append(resturant["longitude"])

        return Resturant(*params)

    def to_dict(self):
        return {
            "address" : self.address,
            "categories" : self.categories,
            "finished" : self.finished,
            "link" : self.link,
            "name" : self.name,
            "num" : self.num,
            "state" : self.state,
            "zip_code" : self.zip_code,
            "latitude" : self.latitude,
            "longitude" : self.longitude
        }

    def __eq__(self, other):
        try:
            return self.__dict__ == other.__dict__
        except:
            return False

    def web_safe_address(self):
        splitAddress = self.address.replace(".", "").split(" ")[:-1]
        seperator="+"
        return seperator.join(splitAddress)
        
        