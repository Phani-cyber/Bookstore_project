import os
import json
from random import choice, randint

from crud import *
import model
import server

os.system('dropdb project')
os.system('createdb project')

model.connect_to_db(server.app)
model.db.create_all()

# Load book data from JSON file
with open('data/books.json') as f:
    book_data = json.loads(f.read())

print()


# Create books, store them in list so we can use them
books_in_db = []
#author_id = get_author_id('test','test')
#print(author_id)
for book in book_data:
    author_name = book['author'].split(' ')
    print(author_name)
    
    if(existing_author(author_name[0], author_name[1]) == True):
        db_author = create_author(author_name[0],author_name[1])

for book in book_data:
    author_name = book['author'].split(' ')
    print(author_name)
    author_id = get_author_id(author_name[0],author_name[1])
    print(author_id)
    title,genre,price,author  = (book['title'],
                                   book['genre'],
                                   book['price'],author_id)


    print("title,genre,price,author",title,genre,price,author)

    db_book = create_book(title,genre,price,author)
    
    books_in_db.append(db_book)


## Create users
create_user('Josh','Chen','josh.chen@email.com', 'test')
create_user('Neena','Kochar','neena@email.com', 'test')
create_user('Steven','King','steven.king@email.com', 'test')
create_user('Nancy','Greenberg','nancy.greengerg@email.com', 'test')
create_user('Lex','Joe','lex.joe@email.com', 'test')
create_user('Alexander','Horald','alex.horald@email.com', 'test')
create_user('Valli','Pataballa',"valli@email.com", 'test')
create_user('David','Austin','david@email.com', 'test')
create_user('Bruce','Ernst','bruce.ernst@email.com', 'test')
create_user('Daniel','Farve','daniel.farve@email.com','test')



## Add orders
create_order(1,20)
create_order(1,30)

#add order item
create_order_item(1,1,2)
create_order_item(2,2,3)

##Add ratings
create_rating(2,1,1)
create_rating(3,2,2)





