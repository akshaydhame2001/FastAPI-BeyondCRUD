from fastapi import FastAPI, Header, status, Response
from fastapi.exceptions import HTTPException
from typing import Optional, List
from pydantic import BaseModel

app = FastAPI()

books = [
    {
      "id": 1,
      "title": "Think Python",
      "author": "Allen B. Downey",
      "publisher": "O'Reilly Media",
      "published_date": "2021-01-01",
      "page_count": 1234,
      "language": "English"
    },
    {
      "id": 2,
      "title": "Django By Example",
      "author": "Antonio Mele",
      "publisher": "Packt Publishing Ltd",
      "published_date": "2022-01-19",
      "page_count": 1023,
      "language": "English"
    },
    {
      "id": 3,
      "title": "Fluent Python",
      "author": "Luciano Ramalho",
      "publisher": "O'Reilly Media",
      "published_date": "2015-08-04",
      "page_count": 792,
      "language": "English"
    },
    {
      "id": 4,
      "title": "Python Crash Course",
      "author": "Eric Matthes",
      "publisher": "No Starch Press",
      "published_date": "2019-05-03",
      "page_count": 544,
      "language": "English"
    },
    {
      "id": 5,
      "title": "Effective Python",
      "author": "Brett Slatkin",
      "publisher": "Addison-Wesley Professional",
      "published_date": "2019-12-03",
      "page_count": 312,
      "language": "English"
    },
    {
      "id": 6,
      "title": "Clean Code",
      "author": "Robert C. Martin",
      "publisher": "Prentice Hall",
      "published_date": "2008-08-01",
      "page_count": 464,
      "language": "English"
    }
  ]

class Book(BaseModel):
    "id": int
    "title": str
    "author": str
    "publisher": str
    "published_date": str
    "page_count": int
    "language": str

class BookUpdateModel(BaseModel):
    "title": str
    "author": str
    "publisher": str
    "page_count": int
    "language": str

@app.get('/')
async def read_root():
    return {"message": "Hello World"}

# Path parameter /greet/Akshay
# @app.get('/greet/{name}')
# async def greet_name(name:str) -> dict:
#     return {"message": f"Hello {name}"}

# Query parameter /greet?name=AD
# @app.get('/greet')
# async def greet_name(name:str) -> dict:
#     return {"message": f"Hello {name}"}

# Path+Query parameter /greet/Akshay?age=24
# dict return type hint
# json.stringify() -> json.dumps(), json.parse() -> json.loads()
# @app.get('/greet/{name}')
# async def greet_name(name:str, age:int) -> dict:
#     return {"message": f"Hello {name}", "age":age}

# Optional /greet?name=Akshay&age=24
# first non default args then default args
@app.get('/greet')
async def greet_name(name:Optional[str] = "User", age:int = 0) -> dict:
    return {"message": f"Hello {name}", "age":age}

# Serialization/Schema Model
class BookCreateModel(BaseModel):
    title: str
    author: str

@app.post('/create-book')
async def create_book(book_data:BookCreateModel):
    return {
        "title": book_data.title,
        "author": book_data.author
    }

@app.get('/get_headers', status_code=200)
async def get_headers(
    accept:str = Header(None),
    content_type:str = Header(None),
    user_agent:str = Header(None),
    host:str = Header(None)
): 
    request_headers = {}
    request_headers["Accept"] = accept
    request_headers["Content-Type"] = content_type
    request_headers["User-Agent"] = user_agent
    request_headers["Host"] = host

    return request_headers

@app.get('/books', response_model=List[Book])
async def get_all_books() -> list:
    return books

@app.post('/books', status_code=status.HTTP_201_CREATED)
async def create_a_book(book_data:Book) -> dict:
    new_book =book_data.model_dump()
    books.append(new_book)
    return new_book

@app.get('/books/{book_id}')
async def get_a_book(book_id:int) -> dict:
    for book in books:
        if book['id'] == book_id:
            return book
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found"
        )

@app.patch('/books/{book_id}')
async def update_book(book_id:int, book_update_data:BookUpdateModel) -> dict:
    for book in books:
        if book['id'] == book_id:
            book['title'] = book_update_data.title
            book['publisher'] = book_update_data.publisher
            book['page_count'] = book_update_data.page_count
            book['language'] = book_update_data.language

            return book
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found"
        )

@app.delete('/books/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id:int):
    for book in books:
        if book['id'] == book_id:
            books.remove(book)

            return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found"
        )