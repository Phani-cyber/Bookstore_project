from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Book(db.Model):
    """A book."""

    __tablename__ = 'books'

    book_id = db.Column(db.Integer,autoincrement=True, nullable=False ,primary_key=True)
    title = db.Column(db.String(200),nullable=False)
    genre = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer , nullable=False)
    author_id  = db.Column(db.Integer,db.ForeignKey('authors.author_id'),nullable=False)
    image  = db.Column(db.String(100),nullable = False)
    def __repr__(self):
        return f'<Book.book_id={self.book_id} title={self.title}>'  


class Author(db.Model):
    """A author."""

    __tablename__ = 'authors'

    author_id = db.Column(db.Integer, autoincrement=True,nullable=False, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f'<Author.author_id={self.author_id} first_name={self.first_name} last_name={self.last_name}>'


# class Order_Item(db.Model):
#     """A order_item."""

#     __tablename__ = 'order_items'

#     order_id = db.Column(db.Integer, autoincrement=True,nullable=False, primary_key=True)
#     book_id = db.Column(db.Integer,nullable=False)
#     quantity = db.Column(db.Integer,nullable=False)
#     def __repr__(self):
#         return f'<Order_Item.order_item_id={self.order_item_id} quantity={self.quantity}>'  

class Order(db.Model):
    """A order."""

    __tablename__ = 'orders'

    order_id = db.Column(db.Integer, autoincrement=True,nullable=False,primary_key=True)
    user_id = db.Column(db.Integer,nullable=False)
    book_id = db.Column(db.Integer,nullable=False)
    quantity = db.Column(db.Integer,nullable=False)
    total = db.Column(db.Integer,nullable=False)

    def __repr__(self):
        return f'<Order order_id={self.order_id} total={self.total}>'     

     
class User(db.Model):
    """A user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name  = db.Column(db.String,nullable=False)
    last_name = db.Column(db.String,nullable=False)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String,nullable=False)
    
    def __repr__(self):
        return f'<User first_name={self.first_name} last_name={self.last_name} user_id={self.user_id} email={self.email} password={self.password}>'


    
class Rating(db.Model):
    """A movie rating."""

    __tablename__ = 'ratings'

    rating_id = db.Column(db.Integer, autoincrement=True,nullable=False,primary_key=True)
    rating= db.Column(db.Integer,nullable=False)
    book_id = db.Column(db.Integer,db.ForeignKey('books.book_id'),nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('users.user_id'),nullable=False)

    book = db.relationship('Book', backref='ratings')
    user = db.relationship('User', backref='ratings')

    def __repr__(self):
        return f'<Rating rating_id={self.rating_id} rating={self.rating}>'             



def connect_to_db(flask_app, db_uri='postgresql:///project', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')






if __name__ == '__main__':
    
    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.
    #from flask import Flask
    from server import app

    #app = Flask(__name__)

    connect_to_db(app)
