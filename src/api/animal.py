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
def create_animal(animal_name: str, attack: int, defense: int):
    # create an animal with animal name, attack and defense
    # price is equal to sum of the stats

    with db.engine.begin() as connection:
        animal_id = connection.execute(sqlalchemy.text("""INSERT INTO animals (name, attack, defense, price) 
                                           VALUES (:animal_name, :attack, :defense, :price) RETURNING animal_id"""), 
                                           [{"animal_name": animal_name, "attack": attack,
                                            "defense": defense, "price": attack + defense}]).one().animal_id
        
        # update starting health in transactions
        connection.execute(sqlalchemy.text("""INSERT INTO transactions (animal_id, health, description) 
                                                       VALUES (:animal_id, :health, :description)"""),
                                                        [{"animal_id": animal_id, "health": 100, "description": "create animal"}])



    return f"created animal id {animal_id}: {animal_name}, {attack}, {defense}" # animal_id


@router.post("/buy-animal/{animal_name}")
def buy_animal(animal_id: int, animal_name: str, user_id: int):
    status = False
    with db.engine.begin() as connection:
        try:
            # find user's gold
            user = connection.execute(sqlalchemy.text("SELECT SUM(gold) AS gold FROM transactions WHERE user_id = :user_id"), [{"user_id": user_id}]).one()
            
            # find price of animal
            animal = connection.execute(sqlalchemy.text("SELECT user_id, price FROM animals WHERE animal_id = :animal_id"), [{"animal_id": animal_id}]).one()

            if user.gold > animal.price:
                print("user can afford animal")

                # check if unowned
                if(animal.user_id is None):
                    print("animal is available")

                    # TODO: check if user already has an animal
                    # if so, unassign the user_id from that animal by setting it to NULL 
                    # and reset animal health to 100 by finding the difference between 100 
                    # and current health and adding that to transations

                    # insert into transactions 
                    connection.execute(sqlalchemy.text("""INSERT INTO transactions (user_id, gold, description) 
                                                       VALUES (:user_id, -:gold, :description)"""),
                                                        [{"user_id": user_id, "gold": animal.price, "description": "buy animal"}])

                    # update animal to user link
                    connection.execute(sqlalchemy.text("UPDATE users SET animal_id = :animal_id WHERE user_id = :user_id"), [{"animal_id": animal_id, "user_id": user_id}])
                    connection.execute(sqlalchemy.text("UPDATE animals SET user_id = :user_id WHERE animal_id = :animal_id"), [{"user_id": user_id, "animal_id": animal_id}])
                    status = True
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