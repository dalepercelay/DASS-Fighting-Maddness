from sqlite3 import IntegrityError
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db

# create animal
# buy animal

router = APIRouter(
    prefix="/animal",
    tags=["animal"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.post("/buy-animal/{animal_name}")
def buy_animal(animal_name: str, user_name: str):
    status = False
    with db.engine.begin() as connection:
        try:
            user = connection.execute(sqlalchemy.text("SELECT gold, id FROM users WHERE name = :user_name"), [{"user_name": user_name}])
            price = connection.execute(sqlalchemy.text("SELECT price FROM animals WHERE name = :animal_name"), [{"animal_name": animal_name}])
            user = user.fetchone()
            price = price.fetchone()[0]
            # if user can afford buying that animal
            if user[0] >= price:
                description = 'bought ' + animal_name
                connection.execute(sqlalchemy.text("INSERT INTO transactions (user_id, user_name, money, description) VALUES (:user_id, :user_name, -:money, :description)"), [{"user_id": user[1], "user_name": user_name, "money": price, "description": description}])
                connection.execute(sqlalchemy.text("UPDATE animals SET availability = FALSE WHERE name = :animal_name"), [{"animal_name": animal_name}])
                status = True
        except IntegrityError:
            return "INTEGRITY ERROR!"
    
    return {"delivery_status": status}