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
            id = connection.execute(sqlalchemy.text("INSERT INTO users (name, gold) VALUES (:name, 200) RETURNING user_id"), [{"name": name}])
            user_id = id.fetchone()[0]
            connection.execute(sqlalchemy.text("INSERT INTO transactions (user_id, user_name, gold, description) VALUES (:user_id, :user_name, :money, :description)"), [{"user_id": user_id, "user_name": name, "money": 200, "description": "create new user"}])
            print(f"user_id: {user_id}")
        except IntegrityError:
            return "INTEGRITY ERROR!"
    return f"Successfully created a user: {user_id}"

if __name__ == "__main__":
    print(create_user())