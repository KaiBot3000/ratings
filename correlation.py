"""Pearson correlation."""

from math import sqrt


def pearson(pairs):
    """Return Pearson correlation for pairs.

    Using a set of pairwise ratings, produces a Pearson similarity rating.
    """

    series_1 = [float(pair[0]) for pair in pairs]
    series_2 = [float(pair[1]) for pair in pairs]

    sum_1 = sum(series_1)
    sum_2 = sum(series_2)

    squares_1 = sum([n * n for n in series_1])
    squares_2 = sum([n * n for n in series_2])

    product_sum = sum([n * m for n, m in pairs])

    size = len(pairs)

    numerator = product_sum - ((sum_1 * sum_2)/size)

    denominator = sqrt(
        (squares_1 - (sum_1 * sum_1) / size) *
        (squares_2 - (sum_2 * sum_2) / size)
    )

    if denominator == 0:
        return 0

    return numerator / denominator


def make_pairs():

    """
    What we have: list of our ratings, 
                list of users who rated target movie, 
                target movie object

    We want: List of pairs (our rating, their rating) for each other user
                    (this is argument for pearson() )

    # we'll need to change parameter later, since we need to compare w/ multiple users
    m = Movie.query.filter_by(title="Toy Story").one()
    u = User.query.get(1)  

    # list of user(1)'s rating objects
    ratings = u.ratings 

    # list of all ratings Toy Story has received
    other_ratings = Rating.query.filter_by(movie_id=m.movie_id).all()

    # list of all users that have rated Toy Story
    other_users = [r.user for r in other_ratings]

    # for our ratings
        for other other_users
            if they have same movie
                get their score

    # for our ratings
        for other_user 
            if our rating movie id in their list of ratings,
                add both to list as tuple
        

    # for our ratings
        add movie id to dictionary
        for other user add ids to their own dictionary
        zip dicts together, should make list of tuples