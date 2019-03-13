import hashlib

class Resturant:

    def __init__(self, address, categories, finished, link, name, num, state, zip_code):
            self.hashed_name = hashlib.sha224(name.encode("utf-8")).hexdigest()
            self.address = address
            self.categories = categories
            self.finished = finished
            self.link = link
            self.name = name
            self.num = num
            self.state = state
            self.zip_code = zip_code

    @staticmethod
    def from_dict(resturant):
        return Resturant(
            resturant["address"], 
            resturant["categories"], 
            resturant["finished"], 
            resturant["link"], 
            resturant["name"], 
            resturant["num"], 
            resturant["state"], 
            resturant["zip_code"])

    def to_dict(self):
        return {
            "address" : self.address,
            "categories" : self.categories,
            "finished" : self.finished,
            "link" : self.link,
            "name" : self.name,
            "num" : self.num,
            "state" : self.state,
            "zip_code" : self.zip_code
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
        
        