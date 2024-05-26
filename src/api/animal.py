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

@router.post("/create")
def create_animal(animal_name: str, attack: int, defense: int):
    '''Create an animal to be listed in the catalog (price = attack + defense).'''
    # create an animal with animal name, attack and defense
    # price is equal to sum of the stats
    try:
        if int(animal_name):
            return "Please name an animal with the alphabet."
    except ValueError:
        print("Caught ValueError")
    if attack <= 0 or defense <= 0 or attack > 80 or defense > 80:
        return "Please try again. Your inputs are not matching up with the required: 1. Defense and attack must be from 1 through 80. 2. Make sure the name of the animal is unique and isn't a number."
    try:
        with db.engine.begin() as connection:
            # check if animal name exists already before
            try:
                connection.execute(sqlalchemy.text("SELECT COALESCE(name, '-1') FROM animals WHERE UPPER(name) LIKE UPPER(:name)"), {"name": animal_name}).fetchone()[0]
            except TypeError:
                print("Animal is unique")
            else:
                return "Please try again. This name has been used for an animal already."
            
            animal_id = connection.execute(sqlalchemy.text("""INSERT INTO animals (name, attack, defense, price) 
                                            VALUES (:animal_name, :attack, :defense, :price) RETURNING animal_id"""), 
                                            [{"animal_name": animal_name, "attack": attack,
                                                "defense": defense, "price": attack + defense}]).one().animal_id
            
            # update starting health in transactions
            connection.execute(sqlalchemy.text("""INSERT INTO transactions (animal_id, health, description) 
                                                        VALUES (:animal_id, :health, :description)"""),
                                                            [{"animal_id": animal_id, "health": 100, "description": "create animal"}])

    except IntegrityError:
        return "create animal: INTEGRITY ERROR!"

    return f"created animal id {animal_id}: {animal_name}, {attack}, {defense}" # animal_id


@router.put("/buy")
def buy_animal(animal_id: int, user_id: int):
    '''Buy animal (only if you have enough gold)'''
    status = False
    try:
        with db.engine.begin() as connection:
    
            # find user's gold
            user = connection.execute(sqlalchemy.text("SELECT SUM(gold) AS gold FROM transactions WHERE user_id = :user_id"), 
                                      [{"user_id": user_id}]).one()
            
            # find price of animal
            animal = connection.execute(sqlalchemy.text("SELECT in_use, price FROM animals WHERE animal_id = :animal_id"), 
                                        [{"animal_id": animal_id}]).one()

            if user.gold >= animal.price:
                print("user can afford animal")

                # check if unowned
                if(animal.in_use is False):
                    print("animal is available")
                    # check if user already has an animal
                    id = connection.execute(sqlalchemy.text("SELECT animal_id FROM users WHERE user_id = :user_id"), 
                                            [{"user_id": user_id}]).one()
                    if id.animal_id is not None:                        
                        # and reset animal health to 100 by finding the difference between 100
                        health = connection.execute(sqlalchemy.text("SELECT SUM(health) AS total_health FROM transactions WHERE animal_id = :animal_id"), 
                                                    [{"animal_id": id.animal_id}])
                        prev_animal_name = connection.execute(sqlalchemy.text("SELECT name FROM animals WHERE animal_id = :animal_id"), 
                                                              [{"animal_id": id.animal_id}]).one()
                        # and current health and adding that to transations
                        add_back = 100 - int(health.fetchone().total_health)
                        description = "restored health back to 100 for " + prev_animal_name.name
                        connection.execute(sqlalchemy.text("INSERT INTO transactions (animal_id, health, description) VALUES (:animal_id, :add_back, :description)"), 
                                           [{"animal_id": id.animal_id, "add_back": add_back, "description": description}]) 
                        connection.execute(sqlalchemy.text("UPDATE animals SET in_use = False WHERE animal_id = :animal_id"), 
                                           [{"animal_id": id.animal_id}])

                    # insert into transactions 
                    connection.execute(sqlalchemy.text("""INSERT INTO transactions (user_id, gold, description) 
                                                       VALUES (:user_id, -:gold, :description)"""),
                                                        [{"user_id": user_id, "gold": animal.price, "description": "buy animal"}])

                    # update animal to user link
                    connection.execute(sqlalchemy.text("UPDATE users SET animal_id = :animal_id WHERE user_id = :user_id"), 
                                       [{"animal_id": animal_id, "user_id": user_id}])
                    connection.execute(sqlalchemy.text("UPDATE animals SET in_use = True WHERE animal_id = :animal_id"), 
                                       [{"animal_id": animal_id}])

                    status = True

    except IntegrityError:
        return "buy animal: INTEGRITY ERROR!"
    
    return {"delivery_status": status}