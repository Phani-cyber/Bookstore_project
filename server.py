"""Server for bookstore app."""

from flask import Flask
from flask import (Flask, render_template, request, flash, session,
                   redirect, url_for)
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

@app.route('/users', methods=['POST'])
def register_user():
    """Register a new user"""
    first_name = request.form.get('FirstName')
    last_name = request.form.get('LastName')
    email = request.form.get('email')
    password = request.form.get('password')

    user = get_user_by_email(email)
    
    """Check to see if user is already in database"""
    if user:
        flash("This email already exists. Try again")
        return render_template('/')
    else:
        create_user(first_name,last_name,email, password)
        flash("Your account was created successfully")

        return render_template('login.html')

@app.route('/login', methods=['POST'])
def user_login():
    """Log a user into the website"""

    email = request.form.get('email')
    password = request.form.get('password')

    user = check_user_login_info(email, password)
    print(user)

    if user:
        flash("Successful login")
        ##create session here
        return render_template('login.html')
    else:
        flash("Login info incorrect, please try again")
        return render_template('homepage.html')


@app.route("/search", methods=["GET"])
def search():
    return render_template('search.html')

@app.route("/searching", methods=["POST"])
def searching():
    search_word = request.form.get('search')
    search_type = request.form.get('search_by')
    print("Dfasfasdfasdfsdafsdafsdf")
    print(search_word)
    if search_type ==  'author':
        search_result = get_book_by_author(search_word)
        book_id = search_result
        print(search_result)
        return redirect('/books/' + str(book_id))
    if search_type == 'title':
        search_result = get_book_by_title(search_word)
        print(search_result)
        return redirect('/books/' + str(search_result))
    # return render_template('search.html')
    

     


    
    






if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)