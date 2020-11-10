import os
import json
from random import choice, randint

from crud import *
import model
import server

os.system('dropdb ratings')
os.system('createdb ratings')

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
    #print("alsjdflasdjfjaolksdjflka;sdjflas ldkfklsdfjkl")
    db_book = create_author(author_name[0],author_name[1])

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
create_user("John",'Doe','john.doe@email.com', 'test')
create_user('sally','doe',"sally.doe@email.com", 'test')

## Add orders
create_order(1,20)
create_order(1,30)

#add order item
create_order_item(1,1,2)
create_order_item(2,2,3)

##Add ratings
create_rating(2,1,1)
create_rating(3,2,2)





