import operator
import numpy as np

from db.models import Users, Movies, Ratings, MoviesIMDb, UserSimilarity
from db.database import db_session

from scripts import utils




def recommender_list(user):

   return []

def collaborative_filtering(user):

    result_ = recommender_list(user)

    final_list = []

    for movie in result_:
        movie = utils.get_imdb_information(movie[0])
        final_list.append(movie)

    return final_list


if __name__ == "__main__":
    print("Recommender Script")