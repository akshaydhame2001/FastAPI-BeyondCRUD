from fastapi import FastAPI
from typing import Optional

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

