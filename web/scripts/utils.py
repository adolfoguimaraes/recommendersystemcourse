import sys, os

parent_dir_name = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_dir_name)

from db.models import Users, Movies, Ratings, MoviesIMDb, UserSimilarity
from db.database import db_session

def get_all_users():

    """

    :return: a list of ids with all users of dataset
    """

    result_ = db_session.query(Users.id).all()

    return [id for (id, ) in result_]

def pre_get_movies_by_user():

    """

    :return: return a map with movies watched by all users
    """

    all_users = get_all_users()

    movies_user = {}

    for user in all_users:
        movies_user[user] = get_movies_by_user(user)

    return movies_user


def get_all_movies():

    """

    :return: return all movies of database
    """

    result_ = db_session.query(Movies.id).all()

    return result_


def get_most_similar_users(user_id, limit_):

    """

    :param user_id: id of user
    :param limit_: number of similars users to return
    :return: return a list with if of similar users
    """

    result_ = db_session.query(UserSimilarity.id_user_y).filter(UserSimilarity.id_user_x == user_id).order_by("similarity desc").limit(limit_).all()

    return [x[0] for x in result_]


def get_rating_by_user_movie(user_id, movie_id):
    """

    :param user_id: id of user
    :param movie_id: id of movie
    :return: return a value of rating of user_id to movie_id
    """

    result_ = db_session.query(Ratings).filter_by(user_id = user_id, movie_id=movie_id).first()

    if not result_:
        return 0.0

    return float(result_.rating)


def get_users_by_movie(movie_id, rating_cut=0):

    """

    :param movie_id: id of movie
    :param rating_cut: rating cut to return just users that rated a movie gratter than rating_cut (default: 0)
    :return: a list of users that rated a specific movie
    """

    result_ = (db_session.query(Movies, Ratings)
               .filter(Users.id == Ratings.user_id)
               .filter(Movies.id == Ratings.movie_id)
               .filter(Ratings.rating >= rating_cut)
               ).filter(Movies.id == movie_id).all()

    return_dict = {}

    for user in result_:
        return_dict[user[1].user_id] = float("%.2f" % user[1].rating)

    return return_dict


def get_movies_by_user(user_id, rating_cut=0):

    """

    :param user_id: id of user
    :param rating_cut: return just items rated with value bigger than rating_cut (default: 0)
    :return: rerturn a dict of movies rated by using with rating values
    """

    result_ = (db_session.query(Movies, Ratings)
     .filter(Users.id == Ratings.user_id)
     .filter(Movies.id == Ratings.movie_id)
     .filter(Ratings.rating >= rating_cut)
     ).filter(Users.id == user_id).all()

    return_dict = {}

    for movie in result_:
        return_dict[movie[0].id] = float("%.2f" % movie[1].rating)

    return return_dict

def convert_rating_stars(number):

    number = float("%.1f" % number)

    lists = []

    while number > 1.0:
        lists.append(1.0)
        number -= 1

    lists.append(number)

    while len(lists) < 5:
        lists.append(0)

    return lists

def get_imdb_information(movie_id):

    """
    :param movie_id: id of movie
    :return: return a dictionary with the imdb information of a movie
    """

    result = (db_session.query(MoviesIMDb)).filter(MoviesIMDb.id == movie_id).all()

    movie = result[0]


    object_movie = {
            'id': movie.id,
            'title': movie.title,
            'year': movie.year,
            'image_url': movie.image_url,
            'rating': 0,
            'rating_star': convert_rating_stars(0)

        }



    return object_movie