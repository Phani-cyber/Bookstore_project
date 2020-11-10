"""Server for bookstore app."""

from flask import Flask
from flask import (Flask, render_template, request, flash, session,
                   redirect)
from model import connect_to_db
from crud import *
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


# Replace this with routes and view functions!
@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')

@app.route('/books')
def all_books():
    books = get_books()
    print(books)
    return render_template('all_books.html', books=books)

@app.route('/books/<book_id>')
def show_book(book_id):
    book = get_book_by_id(book_id)
    return render_template('book_details.html', book=book)

@app.route('/users')
def all_users():

    users = get_users()

    return render_template('all_users.html',users=users)

@app.route('/users/<user_id>')
def show_user(user_id):
    user = get_user_by_user_id(user_id)
    return render_template('user_details.html', user=user)
   




if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)