import numpy as np
from keras import backend as K

from flaskr.models.resturant import Resturant



def search(m, resturants):
    resturants = [Resturant.from_dict(i.to_dict()) for i in resturants]
    nums = [i.num for i  in resturants]
    nums = np.array(nums)
    ratings = m.predict([np.full_like(nums, 569), nums])
    results = []
    for index, rating in enumerate(ratings):
        highest = rating[0]
        highest_index = 0
        for i, value in enumerate(rating):
            if value > highest:
                highest = value
                highest_index = i
        if highest_index == 4:
            results.append({
                "link" : resturants[index].link,
                "rating" : str(highest)
            })
    K.clear_session()
    return results