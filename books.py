from fastapi import FastAPI

app: FastAPI  = FastAPI()

@app.get("/")
async def first_api() -> dict:
    return {'message': 'Hello Subhrajit'}

@app.get("/ankita")
async def first_api() -> dict:
    return {'message': 'Hello ankita'}

books: list[dict[str,str]] = [
    {'title': 'A Brief History of Time',     'author': 'Stephen Hawking',     'category': 'science'},
    {'title': 'The Selfish Gene',            'author': 'Richard Dawkins',     'category': 'science'},
    {'title': 'Sapiens: A Brief History',    'author': 'Yuval Noah Harari',   'category': 'history'},
    {'title': 'The Man Who Knew Infinity',   'author': 'Robert Kanigel',      'category': 'math'},
    {'title': 'Fermat\'s Enigma',            'author': 'Simon Singh',         'category': 'math'},
    {'title': 'The Code Book',               'author': 'Simon Singh',         'category': 'math'},
    {'title': 'To Kill a Mockingbird',       'author': 'Harper Lee',          'category': 'literature'},
    {'title': '1984',                        'author': 'George Orwell',       'category': 'fiction'},
    {'title': 'Meditations',                 'author': 'Marcus Aurelius',     'category': 'philosophy'},
    {'title': 'The Innovators',              'author': 'Walter Isaacson',     'category': 'technology'}
]

@app.get("/books")
async def get_books() -> dict:
    return {'books': books}
@app.get("/books1")
async def get_books() -> object:
    return books

@app.get("/books/{book_name}") #This is also called Path Parameter and the name of the parameter must be same in both
async def returtn_specific_book(book_name: str) -> dict:
    for book in books:
        if book['title'].lower() == book_name.lower():
            return {'book': book}
    else:
        return {'message': 'Book not found'}
    

#Query Parameter
#We can use query parameter in two ways
#1. 
@app.get("/books/")
async def return_specific_book_using_query(book_title: str) -> dict:
    for book in books:
        if book['title'].lower() == book_title.lower():
            return {'book': book}
    return {'message': 'Book not found'}


#2 .
#You can use Query() to:
#Set defaults
#Add metadata
#Apply validation rules

from fastapi import Query
#Query Parameter
@app.get("/books/query/") #
async def returtn_specific_book_using_query(book_name: str = Query(...,description="Name of the book")) -> dict:
    for book in books:
        if book['title'].lower() == book_name.lower():
            return {'book': book}
    else:
        return {'message': 'Book not found'}

#POST Request
from fastapi import Body #Using Body class we can pass the dict or json of book inside post body
@app.post("/books/create_book/")
async def create_and_add_book(new_book:dict = Body(...,description="New Book")) -> dict:
    books.append(new_book)
    return {'message': f'new books has been added with Name {new_book['title']}'}

#PUT Request to update
@app.put("/books/update_book/")
async def update_book_with_name(updated_book: dict = Body(...)) -> dict:
    for book in books:
        if book['title'].lower() == updated_book['title'].lower():
            book['author'] = updated_book['author']
            book['category'] = updated_book['category']
            return {'message': f"Book {book['title']} has been updated successfully"}
    else:
        return {'message': 'Book not found'}

#Delete Request
@app.delete("/books/delete_book/")
async def delete_book_with_name(book_name: str = Query(..., description="Title of the book to delete")) -> dict:
    for i in range(len(books)):
        if books[i]['title'].lower() == book_name.lower():
            books.pop(i)
            return {'message': f"Book '{book_name}' has been deleted successfully."}
    return {'message': 'Book not found'}


#Assignment
#Create a new API Endpoint that can fetch all books from a specific author 
#using either Path Parameters or Query Parameters.

@app.get("/books/all_books_by_author/")
async def get_all_books_by_specific_author(author_name: str = Query(...,description="Name of the book author")) -> dict:
    all_books: dict = {}
    count: int = 1
    for book in books:
        if book.get('author').lower() == author_name.lower():
            all_books[count] = book
            count += 1
    
    if all_books:
        return {'books': all_books}
    else:
        return {'message': 'Book not found'}
        
                


    
