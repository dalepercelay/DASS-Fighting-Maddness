from sqlite3 import IntegrityError
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/animal",
    tags=["animal"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.post("/create-animal/{name}")
def create_animal():
    return "OK"

@router.post("/buy-animal/{animal_name}")
def buy_animal(animal_id: int, animal_name: str, user_id: int):
    status = False
    with db.engine.begin() as connection:
        try:
            # find user's gold
            user = connection.executesqlalchemy.text("SELECT SUM(gold) AS gold FROM transactions WHERE user_id = :user_id", [{"user_id": user_id}]).one()
            
            # find price of animal
            animal = connection.executesqlalchemy.text("SELECT user_id, price FROM animals WHERE animal_id = :animal_id)", [{"animal_id": animal_id}]).one()

            if user.gold > animal.price:
                print("user can afford animal")


                # check if unowned
                if(animal.user_id is None):
                    print("animal is available")
                    # insert into transactions 
                    connection.execute(sqlalchemy.text("INSERT INTO transactions (user_id, gold, desc) VALUES (:user_id, -:gold, :desc)"), [{"user_id": user[2], "gold": animal.price, "desc": "buy animal"}])

                    # update animal to user link
                    connection.execute(sqlalchemy.text("UPDATE users SET animal_id = :animal_id WHERE user_id = :user_id"), [{"animal_id": animal_id, "user_id": user_id}])
                    connection.execute(sqlalchemy.text("UPDATE animals SET user_id = :user_id WHERE animal_id = :animal_id"), [{"user_id": user_id, "animal_id": animal_id}])

            # user = connection.execute(sqlalchemy.text("SELECT gold, name, user_id FROM users WHERE user_id = :user_id"), [{"user_id": user_id}])
            # price = connection.execute(sqlalchemy.text("SELECT price FROM animals WHERE animal_id = :animal_id AND name = :animal_name"), [{"animal_id": animal_id, "animal_name": animal_name}])
            # user = user.fetchone()
            # price = price.fetchone()[0]
            # # if user can afford buying that animal
            # if user[0] >= price:
            #     description = 'bought ' + animal_name
            #     connection.execute(sqlalchemy.text("INSERT INTO transactions (user_id, user_name, gold, description) VALUES (:user_id, :user_name, -:money, :description)"), [{"user_id": user[2], "user_name": user[1], "money": price, "description": description}])
            #     connection.execute(sqlalchemy.text("UPDATE animals SET availability = FALSE WHERE name = :animal_name"), [{"animal_name": animal_name}])
            #     connection.execute(sqlalchemy.text("UPDATE users SET animal_id = :animal_id WHERE user_id = :user_id AND name = :user_name"), [{"animal_id": animal_id, "user_id": user_id, "user_name": user_name}])
            #     status = True
        except IntegrityError:
            return "INTEGRITY ERROR!"
    
    return {"delivery_status": status}