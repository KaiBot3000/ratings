![image](/static/images/search_screenshot.png)
# Movie Ratings

Movie ratings uses machine learning to predict a user's rating of a movie based on past ratings and similar users, calculated usig Pearson Correlation. This is a (mostly finished) project for Hackbright Academy, and pair-programmed with [Noelle Daly](http://noelledaley.github.io/).
Users can...
  - Log in/out using flask sessions
  - Submit new movie ratings
  - See how other users rate a movie
  - See their predicted rating based on Pearson Correlation
  - See other movies rated by particular users

### The Stack
* [SQLite] - Database contains hundreds of users, movies, and ratings.
* [SQLAlchemy] - An ORM which streamlines database queries
* [Python] - Backend code that manipulates incoming data, controls access to the database, and serves data to the webpage through a framework.
* [Flask] - Lightweight web framework which also provides support for jinja templating
* [HTML] - Displays information on the web
* [CSS] - Styles webpages

### The Data
Movie Ratings is seeded with the [MovieLens 100k](http://www.grouplens.org/node/73) dataset. It consists of 100,000 ratings of 1,700 movies from 1,000 users. This data is stored in a SQLite3 database.
