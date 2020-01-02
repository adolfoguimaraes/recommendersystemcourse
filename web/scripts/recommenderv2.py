import operator
import numpy as np

from db.models import Users, Movies, Ratings, MoviesIMDb, UserSimilarity
from db.database import db_session

from scripts import utils


def get_topneighbors_rateditem(id_user, id_movie, N):

    """

    :param id_user: user id
    :param id_movie: movie id
    :param N: number of users that will return
    :return: return the N-top users most similar to id_user that rated id_movie
    """

    users_movie = db_session.query(Ratings).filter(Ratings.movie_id==id_movie, Ratings.user_id!=id_user).all()

    if not users_movie:
        return []

    similar = []

    for item in users_movie:
        user_ = item.user_id

        similarity_register = db_session.query(UserSimilarity.similarity).filter(UserSimilarity.id_user_x==id_user,
                                                                   UserSimilarity.id_user_y==user_).first()

        if not similarity_register:
            similarity_value = 0.0
        else:
            similarity_value = float(similarity_register[0])

        similar.append((user_, similarity_value))

    sorted_ = sorted(similar, key=operator.itemgetter(1), reverse=True)

    return sorted_[:N]


def predict_rating(id_user, id_movie):

    N = 20

    items_rated_by_user = utils.get_movies_by_user(id_user)
    items_rated_by_user_values = [items_rated_by_user[x] for x in items_rated_by_user]

    mean_user = np.mean(items_rated_by_user_values)

    topN_users = get_topneighbors_rateditem(id_user, id_movie, N)

    sum_ = 0
    sum_k = 0

    for topuser in topN_users:

        user_u = topuser[0]
        similarity = topuser[1]

        rating_user_u = utils.get_rating_by_user_movie(user_u, id_movie)
        items_rated_by_user_u = utils.get_movies_by_user(user_u)

        items_rated_by_user_u_values = [items_rated_by_user_u[x] for x in items_rated_by_user_u]

        mean_user_u = np.mean(items_rated_by_user_u_values)

        sum_ += similarity * (rating_user_u - mean_user_u)

        sum_k += abs(similarity)

    if sum_k == 0:
        k = 0
    else:
        k = 1 / sum_k

    final_rating = mean_user + k * sum_

    return final_rating


def recommender_list(user):

    all_movies_user = set(list(utils.get_movies_by_user(user).keys()))
    all_movies = set([x[0] for x in utils.get_all_movies()])

    all_movies_not_rated = list(all_movies - all_movies_user)

    print("Generating recommeder to %i movies." % len(all_movies_not_rated))

    predict = {}

    for movie in all_movies_not_rated[:30]:
        predict[movie] = predict_rating(user, movie)
        

    sorted_items = sorted(predict.items(), key=operator.itemgetter(1), reverse=False)

    return sorted_items[:6]

def collaborative_filtering(user):

    result_ = recommender_list(user)

    final_list = []

    for movie in result_:
        movie = utils.get_imdb_information(movie[0])
        final_list.append(movie)

    return final_list


if __name__ == "__main__":
    print("Recommender Script")