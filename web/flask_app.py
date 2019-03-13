import os
import sys

from flask import Flask
from flask import render_template

from db.models import Users, Movies, Ratings, MoviesIMDb
from db.database import db_session

from scripts.recommender import collaborative_filtering


app = Flask(__name__)

# Support Functions


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


def get_movies_by_user(user_id):

    result_ = (db_session.query(Movies, MoviesIMDb, Ratings)
               .filter(Users.id == Ratings.user_id)
               .filter(MoviesIMDb.id == Ratings.movie_id)
               .filter(Movies.id == Ratings.movie_id)
               ).filter(Users.id == user_id).all()

    watched_movies = []

    for object_ in result_:
        movie =  object_[0]
        movie_imdb = object_[1]
        movie_ratings = object_[2]

        object_movie = {
            'id': movie.id,
            'title': movie_imdb.title,
            'year': movie_imdb.year,
            'image_url': movie_imdb.image_url,
            'rating': movie_ratings.rating,
            'rating_star': convert_rating_stars(movie_ratings.rating)

        }

        watched_movies.append(object_movie)


    return watched_movies


@app.route('/recommender/<user_id>')
def recommender_page(user_id):

    watched_user = get_movies_by_user(user_id)

    collaborative_recommender = collaborative_filtering(user_id)

    args = {
        'user_id': user_id,
        'watched_user': watched_user,
        'collaborative_recommender': collaborative_recommender
    }

    return render_template("recommender.html", args=args)

@app.route('/')
def home():

    args = {}

    return render_template("index.html", args=args)

if __name__ == "__main__":
    app.debug = True
    app.run()