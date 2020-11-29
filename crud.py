#from model import db, Book,Author,User,Order_Item,Order,Rating, connect_to_db
from model import db, Book,Author,User,Order,Rating, connect_to_db

# Functions start here!

def create_user(first_name,last_name,email, password):
    """Create and return a new user."""
    user = User(first_name=first_name,last_name=last_name,email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return user

def get_user_by_user_id(user_id):
    
    user = User.query.get(user_id)

    return user

def get_users():
    return User.query.all()

def get_author_name_by_id(authorid):
    """Return a user by email."""
    return Author.query.filter(Author.author_id == authorid).all()

def get_author_id(first_name,last_name):
    id = db.session.query(Author).filter(Author.first_name == first_name, Author.last_name == last_name).first()

    return id.author_id

def create_author(first_name,last_name):
    author = Author(first_name= first_name,last_name=last_name)
    db.session.add(author)
    db.session.commit()
    return author

def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).all()

def get_authors():
    return Author.query.all()

def existing_author(first_name, last_name):
    author =  Author.query.filter(Author.first_name == first_name, Author.last_name == last_name).all()
    if(len(author) == 0):
        return True
    else:
        return False


def create_book(title,genre,price,author_id):
    book= Book(title=title,genre=genre,price=price,author_id=author_id)
    db.session.add(book)
    db.session.commit()
    return book

def get_books():
    return Book.query.all()

def get_book_by_title(title):
    """Return book by title."""
    result = Book.query.filter(Book.title == title).first()
    return result.book_id

def search_book_by_title(title):
    search = "%{}%".format(title)
    result = Book.query.filter(Book.title.ilike(search)).all()
    return result

def get_book_by_author(name):
    """ Return book by author"""
    name = name.split(' ')
    ## get author id from first and last name
    author =  Author.query.filter(Author.first_name == name[0], Author.last_name == name[1]).all()

    ## Get all books that have author_id equal to author returned by above
    result = Book.query.filter(Book.author_id == author[0].author_id).all()

    return result

## Need to search by first or last name
def search_by_author_name(name):
    """ Return book by author"""
    name = name.split(' ')
    ## get author id from first and last name
    if(len(name) == 1):
        search = "%{}%".format(name[0])
        author =  Author.query.filter((Author.first_name.ilike(search))|(Author.last_name.ilike(search))).all()
    elif(len(name) == 2):
        search = "%{} {}%".format(name[0], name[1])
        author =  Author.query.filter((Author.first_name.ilike(search))|(Author.last_name.ilike(search))).all()

    ## Get all books that have author_id equal to author returned by above
    result = []
    author_name = []
    for id in range(len(author)):
        book_info = Book.query.filter(Book.author_id == author[id].author_id).all()
        name = author[id].first_name + " " + author[id].last_name
        author_name.append(name)
        for books in range(len(book_info)):
            result.append(book_info[books])
    return result, author_name


    
def get_book_by_id(book_id):
    book = Book.query.get(book_id)
    return book
  

def create_order_item(order_id,book_id,quantity):
    order_item = Order_Item(order_id=order_id,book_id=book_id,quantity=quantity)
    db.session.add(order_item)
    db.session.commit()
    return order_item

def get_order_items():
    return Order_Item.query.all()

def create_order(user_id, book_id, quantity, total):
    order = Order(user_id = user_id, book_id = book_id, quantity = quantity, total = total)
    db.session.add(order)
    db.session.commit()
    return order

def get_order_history(user_id):
    order = Order.query.filter(Order.user_id == user_id).all()
    return order

# def create_order(user_id,total):

#     order = Order(user_id=user_id,total=total)
#     return order

def get_order():
    return Order.query.all()


def rating_by_id(book_id):
    ratings = Rating.query.filter(Rating.book_id == book_id).all()
    return ratings

def check_user_login_info(email, password):
    """check if the users email and password match in the database"""

    return User.query.filter((User.email == email) & (User.password == password)).all()    


def create_rating(rating,book_id,user_id):
    rating = Rating(rating=rating,book_id=book_id,user_id=user_id)
    db.session.add(rating)
    db.session.commit()
    return rating

def get_rating():
    return Rating.query.all()

if __name__ == '__main__':
    from server import app
    connect_to_db(app)
    
    #app = Flask(__name__)

 