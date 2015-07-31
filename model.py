"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy
from correlation import pearson

# This is the connection to the SQLite database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of ratings websites."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    zipcode = db.Column(db.String(15), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s email=%s>" % (self.user_id, self.email)

    def find_similarity(self, other_user):

        """
        What we have: list of our ratings, 
                    list of users who rated target movie, 
                    target movie object

        We want: List of pairs (our rating, their rating) for each other user
                        (this is argument for pearson() )
        """

        # list of user(1)'s rating objects
        ratings = self.ratings 

        
        u_ratings = {}

        # Iterate through self's rating objects 
        for r in ratings:

            # Add that rating's movie ID and score to our rating dictionary
            u_ratings[r.movie_id] = r.score
        
        paired_ratings = []

        # Create a list of the other users's rating objects
        ou_ratings = other_user.ratings

        for r in ou_ratings:
            # use their movie_id to find our rating from our dict
            u_rating = u_ratings.get(r.movie_id)

            if u_rating is not None:
                # add both scores to pair, add pair to list
                pair = (u_rating, r.score)
                paired_ratings.append(pair)

        similarity = pearson(paired_ratings)

        return similarity

    def similar_user(self, movie_id):

        # m = Movie.query.get(movie_id)

        # list of all ratings Toy Story has received
        other_ratings = Rating.query.filter_by(movie_id=movie_id).all()

        # list of all user objects that have rated Toy Story
        other_users = [r.user for r in other_ratings]
        
        similarity_scores = []
        for user in other_users:
            result = self.find_similarity(user)
            similarity_scores.append((result, user.user_id))

        sorted_similarity_scores = sorted(similarity_scores, reverse=True)

        similar_user = sorted_similarity_scores[0]

        return similar_user

class Movie(db.Model):
    """Movies available for rating."""

    __tablename__ = "movies"

    movie_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(64))
    released_at = db.Column(db.DateTime)
    imdb_url = db.Column(db.String(128))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Movie movie_id=%s title=%s>" % (self.movie_id, self.title)


class Rating(db.Model):
    """User ratings for movies."""

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.movie_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    score = db.Column(db.Integer)

    # defines relationships to other tables in same db
    user = db.relationship("User", backref=db.backref("ratings", order_by=rating_id))
    movie = db.relationship("Movie", backref=db.backref("ratings", order_by=rating_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Rating rating_id=%s movie_id=%s user_id=%s>" % (self.rating_id, self.movie_id, self.user_id)


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ratings.db'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."