from sqlite3 import IntegrityError
from fastapi import APIRouter, Depends
from enum import Enum
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db

# create user

router = APIRouter(
    prefix="/user",
    tags=["user"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.post("/create-user")
def create_user(name: str):
    # create a user
    with db.engine.begin() as connection:
        try:
            id = connection.execute(sqlalchemy.text("INSERT INTO users (name) VALUES (:name) RETURNING user_id"), [{"name": name}])
            user_id = id.fetchone()[0]
            connection.execute(sqlalchemy.text("INSERT INTO transactions (user_id, gold, description) VALUES (:user_id, :gold, :description)"), [{"user_id": user_id, "gold": 200, "description": "starting gold"}])
            print(f"user_id: {user_id}")
        except IntegrityError:
            return "INTEGRITY ERROR!"
    return f"Successfully created a user: {user_id}"

@router.post("/get-inventory")
def get_inventory(user_id: int):
    # TODO: 
    # return sum gold, animal name, animal health

    return "OK"

if __name__ == "__main__":
    print(create_user())