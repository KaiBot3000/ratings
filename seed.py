"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from model import User, Rating, Movie, connect_to_db, db
from server import app


def load_users():
    """Load users from u.user into database."""

    # open file/read it
    f = open("seed_data/u.user")
    # for every line, save line as variable/


    for line in f:
    # seperate by commas
        split_line = line.split("|")
        if split_line[0] == '10':
            break
        print "line:%s" % split_line  #testing output
        # make new class
        new_user = User(user_id=split_line[0], age=split_line[1], zipcode=split_line[4])
        print "user_id:%s" % split_line[0] 
        print "age:%s" % split_line[1]
        print "zip:%s" % split_line[4]
            # add attributes by index
        print "user:%s" % new_user #check!


        # add to session
        #db.session.add(new_user)
    # session.commit    
    #db.session.commit()


def load_movies():
    """Load movies from u.item into database."""


def load_ratings():
    """Load ratings from u.data into database."""


if __name__ == "__main__":
    connect_to_db(app)

    load_users()
    load_movies()
    load_ratings()
