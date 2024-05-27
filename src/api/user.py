from sqlite3 import IntegrityError
from fastapi import APIRouter, Depends
from enum import Enum
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/user",
    tags=["user"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.post("/create-user")
def create_user(name: str):
    '''Create a user.'''
    # create a user
    try:
        with db.engine.begin() as connection:
            try:
                # supabase is set up so that name can only be unique values
                id = connection.execute(sqlalchemy.text("INSERT INTO users (name) VALUES (:name) RETURNING user_id"), [{"name": name}])
            except:
                return "Username is already in use."

            user_id = id.fetchone()[0]
            connection.execute(sqlalchemy.text("INSERT INTO transactions (user_id, gold, description) VALUES (:user_id, :gold, :description)"), 
                               [{"user_id": user_id, "gold": 200, "description": "starting gold"}])
            print(f"user_id: {user_id}")
    except IntegrityError:
        return "create user: INTEGRITY ERROR!"
    
    return {"user_id": user_id}

if __name__ == "__main__":
    print(create_user())