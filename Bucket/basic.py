from fastapi import FastAPI, Header
from typing import Optional
from pydantic import BaseModel


app = FastAPI()


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

