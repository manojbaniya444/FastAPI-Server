from fastapi import FastAPI, Header
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

user_list = [
    "Jerry"
]

class UserSchema(BaseModel):
    username: str
    email: str

@app.get("/") # simple get request
async def read_root():
    return {"message": "Hello from the server"}

@app.get("/greet/{username}") # Path parameter
async def greet(username: str):
    return {"message": f"Hello {username}"}

@app.get("/search") # query parameters
async def search_for_user(username: str):
    for user in user_list:
        if username in user_list:
            return {"message": f"Details for user {username}"}
        else:
            return {"message": "User not found"}
        
@app.get("/greet_optional")
async def greet(username: Optional[str]="User"):
    return {"message": f"Hello {username}"}

@app.post("/create_user")
async def create_user(user_data: UserSchema):
    new_user = {
        "username": user_data.username,
        "email": user_data.email
    }
    return {"messages": "New User created successfully", "user": new_user}

@app.get("/get_headers")
async def get_all_request_headers(
    user_agent: Optional[str] = Header(None),
    host: Optional[str] = Header(None)
):
    request_headers = {}
    request_headers["user_agent"] = user_agent
    request_headers["host"] = host
    
    return request_headers