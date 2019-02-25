import hashlib


class Resturant():

    def __init__(self, address, categories, finished, link, name, num, state, zip_code):
        self.address = address
        self.categories = categories
        self.finished = finished
        self.link = link
        self.name = name
        self.num = num
        self.state = state
        self.zip_code = zip_code
        self.hashed_name = hashlib.sha224(self.name.encode("utf-8")).hexdigest()

    @staticmethod
    def from_dict(source):
        return Resturant(
            source["address"],
            source["categories"],
            source["finished"],
            source["link"],
            source["name"],
            source["num"],
            source["state"],
            source["zip_code"]
        )

    def to_dict(self):
        return {
            "address"    : self.address,
            "categories" : self.categories,
            "finished"   : self.finished,
            "link"       : self.link,
            "name"       : self.name,
            "num"        : self.num,
            "state"      : self.state,
            "zip_code"   : self.zip_code
        }

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
