from fastapi import FastAPI, HTTPException, status, Query, Path, Body
from typing import Optional, List
from pydantic import BaseModel

app = FastAPI()

# Basic data model for user
class User(BaseModel):
    username: str
    full_name: Optional[str] = None
    active: bool = True

# A dictionary to simulate a database of users
users_db = {}

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI demo server!"}

@app.get("/hello/{name}")
async def greet(name: str = Path(..., title="The name you want to be greeted by")):
    return {"message": f"Hello there, {name}!"}

@app.get("/users/{username}", response_model=User)
async def read_user(username: str):
    if username in users_db:
        return users_db[username]
    raise HTTPException(status_code=404, detail="User not found")

@app.get("/all", response_model=List[User])
async def list_all_users():
    return list(users_db.values())

@app.post("/users/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Username already registered")
    users_db[user.username] = user
    return user

@app.put("/users/{username}")
async def update_user(username: str, user: User):
    if username not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    stored_user_data = users_db[username]
    stored_user_model = User(**stored_user_data)
    update_data = user.dict(exclude_unset=True)
    updated_user = stored_user_model.copy(update=update_data)
    users_db[username] = updated_user
    return updated_user

@app.delete("/users/{username}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(username: str):
    if username not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    del users_db[username]
    return {"message": "User deleted successfully."}
