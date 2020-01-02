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