from fastapi import FastAPI, Query,Body,HTTPException
from starlette import status #For satatus code HTTP
from book import Book


app: FastAPI = FastAPI()

books: list[Book] = [
    Book(id=1, title='A Brief History of Time',     author='Stephen Hawking',     description='A classic on cosmology',             rating=5),
    Book(id=2, title='The Selfish Gene',            author='Richard Dawkins',     description='Groundbreaking work in evolution',  rating=5),
    Book(id=3, title='Sapiens: A Brief History',    author='Yuval Noah Harari',   description='A deep dive into human history',     rating=4),
    Book(id=4, title='The Man Who Knew Infinity',   author='Robert Kanigel',      description='Biography of Ramanujan',             rating=5),
    Book(id=5, title="Fermat's Enigma",             author='Simon Singh',         description='Solving a 300-year-old math puzzle', rating=4),
    Book(id=6, title='The Code Book',               author='Simon Singh',         description='History of cryptography',            rating=4),
    Book(id=7, title='To Kill a Mockingbird',       author='Harper Lee',          description='Classic American novel',             rating=5),
    Book(id=8, title='1984',                        author='George Orwell',       description='Dystopian future',                   rating=5),
    Book(id=9, title='Meditations',                 author='Marcus Aurelius',     description='Stoic philosophy reflections',       rating=4),
    Book(id=10, title='The Innovators',             author='Walter Isaacson',     description='How inventors shaped the digital age', rating=4),
]



@app.get('/books/all_books',status_code=status.HTTP_200_OK)
async def get_books() -> dict:
    return {'books':books}


#Making id of a book unique each time

def get_book_id(book: Book) -> int:
    if len(books) > 0:
        book.id = books[-1].id + 1
    else:
        book.id = 1
    return book
        
#HTTP POST with Paydantic model
@app.post("/books/create_book/")
async def create_book(book: Book) -> dict:
    new_book: Book = Book(**book.model_dump()) #It is for Pydantic2 for lower version **book.dict(). ** operator unpacks and then assigns
    books.append(get_book_id(new_book))
    return {'message': f"Book added {new_book}"}

#Fetch a single book
@app.get("/books/get_book/")
async def get_specific_book(id: int = Query(...,description="Book id")) -> dict:
    for book in books:
        if book.id == id:
            return {'book': book}
    else:
        return {'message': 'Book not found'}

#Fetch all books by Rating
@app.get("/books/get_book_rating/",status_code=status.HTTP_200_OK)
async def get_books_by_rating(rating: int = Query(...,gt=0,lt=5,description="Book ratings")) -> dict:
    all_books: list = []
    for book in books:
        if int(book.rating) == rating:
            print (rating)
            all_books.append(book)
    
    if all_books:
        return {'books': all_books}
    else:
        return {'message': 'Book not found'}

#Update book by id
@app.put("/books/update_book_id/",status_code=status.HTTP_201_CREATED)
async def update_book_by_id(updated_data:Book = Body(...)) -> dict:
    
    for book in books:
        if book.id == updated_data.id:
            book.title = updated_data.title
            book.author = updated_data.author
            book.description = updated_data.description
            book.rating = updated_data.rating
            return {'message': f"Updated {book} successfully..."}
    else:
        raise HTTPException(status_code=404,detail="Book not found")

#Delete book by id
@app.delete("/books/delete_book_id/",status_code=status.HTTP_202_ACCEPTED)
async def delete_book_by_id(id: int = Query(...,gt=0,description="Book id")) -> dict:
    for book in books:
        if book.id == id:
            books.remove(book)
            return {'message': f"Book with id {id} has been deleted successfully..."}
    else:
        raise HTTPException(status_code=404,detail="Book not found")