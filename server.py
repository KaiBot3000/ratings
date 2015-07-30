"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Rating, Movie


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/login')
def show_login():
    """Display form for user to log in or sign up."""

    return render_template('login.html')


@app.route('/logged-in', methods=["POST"])
def login():
    """Allows user to log in."""

    email = request.form.get("email")
    password = request.form.get("password")

    # check if user is in database
    user = User.query.filter_by(email=email).first()

    # if not user:
    #     # Later, let's add separate sign-up page to get info
    #     user = User(email=email, password=password)
    #     db.session.add(user)
    #     db.session.commit()

            # check if password is correct
    # if user.password != password

    session['email'] = email
    session['id'] = user.user_id

    flash("Now logged in as %s" % session['email'])

    return redirect('/users/%s' % session['id'])


@app.route('/add-user', methods=['POST'])
def add_user():
    """Signs user up, adds to database"""

    email = request.form.get("email")
    password = request.form.get("password")
    age = request.form.get("age")
    zipcode = request.form.get("zipcode")


    user = User(email=email, password=password, age=age, zipcode=zipcode)
    db.session.add(user)
    db.session.commit()

    session['email'] = email
    session['id'] = user.user_id

    flash("Now logged in as %s" % session['email'])

    return redirect('/users/%s' % session['id'])


@app.route('/logout')
def logout():
    """Logs user out."""

    del session['email']
    del session['id']
    flash("Logged out")

    return redirect('/')


@app.route('/users')
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route('/users/<int:user_id>')
def user_details(user_id):
    """Show user profile"""

    user = User.query.get(user_id)

    joint_movieratings = db.session.query(Movie.title, 
                                        Movie.movie_id, 
                                        Rating.score).join(Rating)
    
    # returns list of users' ratings in tuple format
    # [(u'River Wild', 3), (u'Rumble in the Bronx', 4)]
    users_ratings = joint_movieratings.filter_by(user_id=user_id).order_by(Movie.title).all()

    return render_template("user.html", user=user, users_ratings=users_ratings)


@app.route('/movies')
def movie_list():
    """Show alphabetical list of movies."""

    show_movies = Movie.query.order_by(Movie.title).all()

    return render_template("movie_list.html", movies=show_movies)


@app.route('/movies/<int:movie_id>')
def movie_details(movie_id):
    """Show movie details"""

    movie = Movie.query.get(movie_id)

    movie_ratings = db.session.query(Rating.score, Rating.user_id).filter_by(movie_id=movie_id).all()

    return render_template("movie.html", movie=movie, movie_ratings=movie_ratings)


@app.route('/submit-rating/<int:movie_id>', methods=['POST'])
def rate_movie(movie_id):

    score = request.form.get('score')

    if 'id' not in session:
        flash('You need to log in first!')
    else:
        new_score = Rating(movie_id=movie_id, user_id=session['id'], score=score)
        db.session.add(new_score)
        db.session.commit()
        flash('You rated that movie a %s' % score)

    return redirect('/movies/%s' % movie_id)



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()