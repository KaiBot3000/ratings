"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from model import User, Rating, Movie, connect_to_db, db
from server import app


def load_users():
    """Load users from u.user into database."""

    f = open("seed_data/u.user")

    for line in f:
        split_line = line.rstrip().split("|")
        new_user = User(user_id=split_line[0], age=split_line[1], zipcode=split_line[4])
        db.session.add(new_user)

    db.session.commit()


def load_movies():
    """Load movies from u.item into database."""

    f = open("seed_data/u.item")

    for line in f:
        split_line = line.rstrip().split("|")
        new_movie = Movie(movie_id=split_line[0], title=split_line[1][:-7], released_at=split_line[2], imdb_url=split_line[3])
        print new_movie.released_at
        print new_movie
        db.session.add(new_movie)

    # db.session.commit()


def load_ratings():
    """Load ratings from u.data into database."""


if __name__ == "__main__":
    connect_to_db(app)

    # load_users()
    load_movies()
    # load_ratings()
