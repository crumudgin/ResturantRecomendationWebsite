class User:

    def __init__(self, num, name):
        self.num = num
        self.name = name

    @staticmethod
    def from_dict(user_dict):
        return User(
            user_dict["num"],
            user_dict["name"]
        )

    def to_dict(self):
        return {
            "num" : self.num,
            "name" : self.name
        }

    def __eq__(self, other):
        try:
            return self.__dict__ == other.__dict__
        except:
            return False