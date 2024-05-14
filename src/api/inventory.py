from sqlite3 import IntegrityError
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import math
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/inventory",
    tags=["inventory"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.get("/audit")
def get_inventory(user_id: int):
    # query in the actual data
    try:
        with db.engine.begin() as connection:
            ids = connection.execute(sqlalchemy.text("SELECT COALESCE(animal_id, -1) FROM users WHERE user_id = :user_id"), [{"user_id": user_id}])
            ids = ids.fetchone()
            gold = connection.execute(sqlalchemy.text("SELECT SUM(gold) FROM transactions WHERE user_id = :user_id"), [{"user_id": user_id}])
            gold = gold.fetchone()
            health = connection.execute(sqlalchemy.text("SELECT SUM(health) FROM transactions WHERE animal_id = :animal_id"), [{"animal_id": ids[0]}])
            health = health.fetchone()
            animal = ids[0]
            if ids[0] != -1:
                # get the animal name
                animal = connection.execute(sqlalchemy.text("SELECT name FROM animals WHERE animal_id = :animal_id"), [{"animal_id": ids[0]}])
                animal = animal.fetchone()[0]
    except IntegrityError:
        return "INTEGRITY ERROR!"
    return {"gold": gold[0], "animal": animal, "animal health": health[0]}

@router.get("/restock")
def restock(user_id: int, gold: int):
    #check if user has enough gold
    with db.engine.begin() as connection:
        try:
            # find user's gold
            user = connection.execute(sqlalchemy.text("""SELECT SUM(gold) AS gold FROM 
                                                      transactions WHERE user_id = :user_id"""), 
                                                      [{"user_id": user_id}]).one()

            if user.gold > gold:
                print("uer has enough gold to restore health")
                health = gold * 2

            # insert into transactions 
            animal_id = connection.execute(sqlalchemy.text("""SELECT animal_id FROM users 
                                                           WHERE user_id = :user_id"""), 
                                                           [{"user_id": user_id}]).one().animal_id


            connection.execute(sqlalchemy.text("""INSERT INTO transactions (user_id, gold, animal_id, health, description) 
                                               VALUES (:user_id, -:gold, :animal_id, :health, :description)"""),
                                                 [{"user_id": user_id, "gold": gold, 
                                                   "animal_id": animal_id, "health": health, 
                                                   "description": "restore health"}])

        except IntegrityError:
            return "INTEGRITY ERROR!"


    return f"restored {health} health with {gold} gold" # gold spent, health restored