from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from models.movies import *
from utils.db import db

app = Flask(__name__)
app.secret_key = "secret_key_for_flash_messages"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)



@app.route('/')
def index():
    return render_template('index.html')


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cast_director = db.Column(db.String(100), nullable=False)
    cast_cast = db.Column(db.String(200), nullable=False)
    cast_country = db.Column(db.String(100), nullable=False)
    movies_title = db.Column(db.String(200), nullable=False)
    movies_description = db.Column(db.Text, nullable=False)
    movies_release_year = db.Column(db.String(4), nullable=False)

    def __repr__(self):
        return f'<Movie {self.movies_title}>'

    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(150), nullable=False, unique=True)
        email = db.Column(db.String(150), nullable=False, unique=True)
        password = db.Column(db.String(150), nullable=False)

@app.route("/movies")
def movies():
    movies = Movie.query.all()
    return render_template("movies.html", movies=movies)

@app.route('/edit-movie/<int:movie_id>', methods=['GET', 'POST'])
def edit_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if request.method == 'POST':
        movie.movies_title = request.form['movies_title']
        movie.cast_director = request.form['cast_director']
        movie.cast_cast = request.form['cast_cast']
        movie.cast_country = request.form['cast_country']
        movie.movies_release_year = request.form['movies_release_year']
        movie.movies_description = request.form['movies_description']

        db.session.commit()
        return redirect(url_for('movies'))

    return render_template('edit.html', movie=movie)

@app.route('/delete_movie/<int:movie_id>', methods=['GET', 'POST'])
def delete_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('movies'))

@app.route("/add-movies", methods=['GET', 'POST'])
def add_movies():
    if request.method == 'POST':
        cast_director = request.form['cast_director']
        cast_cast = request.form['cast_cast']
        cast_country = request.form['cast_country']
        movies_title = request.form['movies_title']
        movies_description = request.form['movies_description']
        movies_release_year = request.form['movies_release_year']
        new_movie = Movie(cast_director=cast_director,
                          cast_cast=cast_cast,
                          cast_country=cast_country,
                          movies_title=movies_title,
                          movies_description=movies_description,
                          movies_release_year=movies_release_year)
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for('movies'))

    return render_template("add_movies.html")

@app.route('/payment')
def payment():
    return render_template('payment.html')

@app.route('/login')
def login():
        return render_template('login.html')

@app.route('/logout')
def logout():
    return render_template('logout.html')


@app.route('/subscription')
def subscription():
         return render_template('subscription.html', subscription=subscription)


@app.route('/submit', methods=['POST'])
def submit():
    director = request.form['Movies_director']
    cast = request.form['Movies_cast']
    country = request.form['Movies_country']
    title = request.form['Movies_title']
    description = request.form['Movies_description']
    release_year = request.form['Movies_release_year']
    movies = request.form.get('id')
    record = Movies.query.get(movies)
    if record:
        record.Movies_title = title
        record.Movies_description = description
        record.Movies_release_year = release_year
        record.Movies_director = director
        record.Movies_cast = cast
        record.Movies_country = country
    else:
        new_movies = Movies(title=title, description=description, release_year=release_year,
                            director=director, cast=cast, country=country)
        db.session.add(new_movies)
    db.session.commit()
    return redirect(url_for('movies'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(
        host='127.0.0.1',
        port=5007,
        debug=True)