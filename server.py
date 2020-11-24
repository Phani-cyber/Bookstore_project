"""Server for bookstore app."""

from flask import Flask
from flask import (Flask, render_template, request, flash, session,
                   redirect, url_for, jsonify)
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

## base route to show book info
@app.route('/books')
def all_books():
    books = get_books()

    ## Get top 5 rated books
    all_books = {}
    book_ids = []
    av_ratings = []
    for book in books:
        ratings = rating_by_id(book.book_id)
        if(len(ratings) == 0):
            continue
        else:
            total = 0
            for items in ratings:
                total += items.rating
            average_rating = total / len(ratings)
            average_rating = round(average_rating, 2)
            all_books[book.book_id] = average_rating

    if(len(all_books) < 5):
        top_books = []
        top_books_rating = []
        for keys in all_books:
            book_info = get_book_by_id(keys)
            top_books.append(book_info)
            top_books_rating.append(all_books[keys])
    else:
        sorted_rating = sorted(all_books.items(), key=lambda kv: kv[1])[:5]
        top_books = []
        top_books_rating = []
        for keys in sorted_rating:
            book_info = get_book_by_id(keys)
            top_books.append(book_info)
            top_books_rating.append(all_books[keys])

    return render_template('all_books.html', books=books, top_books = top_books, top_ratings = top_books_rating)

## Extends base book route to show individual book by book_id
@app.route('/books/<book_id>')
def show_book(book_id):
    book = get_book_by_id(book_id)
    ## Getting ratings from book id
    ratings = rating_by_id(book_id)
    if(len(ratings) == 0):
        rating = "Book has not been rated yet. Be the first to rate after purchase!"
    else:
        total = 0
        for items in ratings:
            total += items.rating
        rating = total / len(ratings)
        rating = round(rating, 2)

    return render_template('book_details.html', book=book, rating=rating)

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
    if (len(user) != 0):
        flash("This email already exists. Try again")
        return redirect('/')
    else:
        create_user(first_name,last_name,email, password)
        flash("Your account was created successfully")

        return render_template('login.html')

@app.route("/login")
def show_login():
    return render_template("login.html")      

@app.route('/login_submit', methods=['POST'])
def login_submit():
    """Log a user into the website"""

    email = request.form.get('name')
    password = request.form.get('email')

    user = check_user_login_info(email, password)
    print(user)
    
    if (len(user) > 0):
        name = user[0].first_name + ' ' + user[0].last_name
        session['user_id'] = user[0].user_id
        session['cart'] = {}
        return jsonify({'login': name})
    
    return jsonify({'invalid': 'Incorrect email or password'}) 


@app.route("/search", methods=["GET"])
def search():
    return render_template('search.html')

@app.route("/searching", methods=["POST"])
def searching():
    search_word = request.form.get('search')
    search_type = request.form.get('search_by')
    print("**********")
    print(search_word)
    if search_type ==  'author':
        search_result = get_book_by_author(search_word)
        book_id = search_result
        print(search_result)
        return render_template('all_books.html', books=book_id)
    if search_type == 'title':
        search_result = get_book_by_title(search_word)
        print(search_result)
        return redirect('/books/' + str(search_result))
        #return render_template('search.html')

@app.route('/add_to_cart',methods=["POST"])
def add_to_cart():
    book_id = request.form.get('book_id')
    quantity = request.form.get('quantity')

    book = get_book_by_id(book_id)
    current_cart = session['cart']
    if(book_id not in current_cart):
        current_cart[book_id] = quantity
    else:
        current_cart[book_id] = current_cart[book_id] + quantity
    session['cart'] = current_cart
    print(current_cart)
    return render_template('book_details.html', book=book)

@app.route("/cart")
def shopping_cart():
    if "cart" not in session:
        flash("There is nothing in your cart.")
        return render_template("cart.html", display_cart = {}, total = 0)
    current_cart = session['cart']
    dict_of_books = {}
    total_price = 0
    ## getting user info
    user = User.query.get(session['user_id'])
    user_name = user.first_name + ' ' + user.last_name
    for books in current_cart:
        book_id = books
        ## Get book info from book_id
        book = get_book_by_id(book_id)
        book_details = {'title': book.title, 'price': book.price}
        ## Add book.price * quantity to total_price
        total_price += book.price * int(current_cart[books])
        dict_of_books[book_id] = book_details

    return render_template("cart.html", display_cart = dict_of_books, total = total_price, user_info = user_name)

@app.route('/purchase',methods=["POST"])
def purchase():
    ## TODO: Check for existing entries for books being rebought and update quantity and price
    user_id = session['user_id']
    print('asdhflsajdfljasldfjkals jflasjlflsdkjf')
    print('userid' + str(user_id))
    cart = session['cart']
    user = User.query.get(session['user_id'])
    user_name = user.first_name + ' ' + user.last_name
    dict_of_books = {}
    total_price = 0
    for book in cart:
        book_id = book
        quantity = cart[book]
        ## Get book price
        book = get_book_by_id(book_id)
        price = book.price
        total = 0
        for i in range(int(quantity)):
            total += price
        print(total)
        ## adding data to table.
        create_order(user_id, book_id, quantity, total)
        total = 0
    return render_template("cart.html", display_cart = dict_of_books, total = total_price, user_info = user_name)

@app.route('/purchase_history')
def purchase_history():
    if "cart" not in session:
        flash("There is nothing in your cart.")
        return render_template("cart.html", display_cart = {}, total = 0)
    dict_of_books = {}
    ## getting user info
    user = User.query.get(session['user_id'])
    user_name = user.first_name + ' ' + user.last_name
    ##Get order history by user_id
    order = get_order_history(session['user_id'])
    dict_of_books = {}
    total_price = 0
    for i in range(len(order)):
        total_price += order[i].total
        book = get_book_by_id(order[i].book_id)
        details = {'book_id': order[i].book_id, "title": book.title, "quantity": order[i].quantity, 'total': order[i].total}
        dict_of_books[i] = details


    return render_template("purchase.html", display_cart = dict_of_books, total = total_price, user_info = user_name)

@app.route('/rating')
def rate_book():
    if "cart" not in session:
        flash("There is nothing in your cart.")
        return render_template("cart.html", display_cart = {}, total = 0)
    dict_of_books = {}
    ## getting user info
    user = User.query.get(session['user_id'])
    user_name = user.first_name + ' ' + user.last_name
    ##Get order history by user_id
    order = get_order_history(session['user_id'])
    dict_of_books = {}
    total_price = 0
    for i in range(len(order)):
        total_price += order[i].total
        book = get_book_by_id(order[i].book_id)
        details = {'book_id': order[i].book_id, "title": book.title, "quantity": order[i].quantity, 'total': order[i].total}
        dict_of_books[i] = details


    return render_template("rating.html", display_cart = dict_of_books, total = total_price, user_info = user_name)

@app.route('/add_rating',methods=["POST"])
def add_rating():
    if "cart" not in session:
        flash("There is nothing in your cart.")
        return render_template("cart.html", display_cart = {}, total = 0)
    dict_of_books = {}

    ## getting user info
    user = User.query.get(session['user_id'])
    user_name = user.first_name + ' ' + user.last_name
    ##Get order history by user_id
    order = get_order_history(session['user_id'])
    dict_of_books = {}
    total_price = 0
    for i in range(len(order)):
        total_price += order[i].total
        book = get_book_by_id(order[i].book_id)
        details = {'book_id': order[i].book_id, "title": book.title, "quantity": order[i].quantity, 'total': order[i].total}
        dict_of_books[i] = details

    book_id = request.form.get('book_id')
    ratings = request.form.get('rating')
    user_id = session['user_id']
    add_rating = create_rating(ratings,book_id,user_id)
    return render_template("rating.html", display_cart = dict_of_books, total = total_price, user_info = user_name)
# @app.route("/add_to_cart/<int:id>")
# def add_to_cart(id):
#     if "cart" not in session:
#         session["cart"] = []

#     session["cart"].append(id)

#     flash("Successfully added to cart!")
#     return redirect("/cart")

@app.route('/top_rated',methods=["POST"])
def top_rated():
    return True

@app.route('/remove_from_cart',methods=["POST"])
def remove_from_cart():
    return True

@app.route('/rating_search',methods=["POST"])
def rating_search():
    return True

@app.route('/logout')
def logout():
    session['user_id'] = ''
    session['cart'] = []
    
    return redirect('/')
    #return True 


    
    






if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)