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

# fix where it shows all animals and their respective healths
@router.get("/inventory")
def get_inventory(user_id: int):
    '''Returns the gold of the user, as well as the animal and animal health (if owned).'''
    # query in the actual data    
    try:
        with db.engine.begin() as connection:
            ids = connection.execute(sqlalchemy.text("SELECT animal_id FROM animals_owned WHERE user_id = :user_id"), [{"user_id": user_id}])
            animal_ids = []
            if ids is None:
                return f"animal_id of {user_id} doesn't exist"
            else:
                for id in ids:
                    animal_ids.append(id.animal_id)

            animals = []
            gold = connection.execute(sqlalchemy.text("SELECT SUM(gold) AS total_gold FROM transactions WHERE user_id = :user_id"), [{"user_id": user_id}]).fetchone()
            if len(animal_ids) > 0:
                for i in animal_ids:
                    # get the animal name
                    animal = connection.execute(sqlalchemy.text("SELECT name FROM animals WHERE animal_id = :animal_id"), [{"animal_id": i}]).fetchone()[0]
                    health = connection.execute(sqlalchemy.text("SELECT SUM(health) FROM transactions WHERE animal_id = :animal_id"), [{"animal_id": i}]).fetchone()[0]
                    animals.append({"animal_id": i, "animal_name": animal, "health": health})
            else:
                animals = "No animal in inventory"
                # animal = "No animal in inventory"
                # health = "No animal health"
    except IntegrityError:
        return "get_inventory: INTEGRITY ERROR!"
    return {"gold": gold.total_gold, "animals": animals}


# fix where you can pick to restock which animal
@router.get("/restore")
def restore_health(user_id: int, animal_id: int, gold: int):
    '''Use gold to restore owned animal's health. 1 gold restores 2 health to a max of 100 health.'''
    #check if user has enough gold
    try:
        with db.engine.begin() as connection:
            # first find out if an animal exists for user
            try:
                animal_id_result = connection.execute(sqlalchemy.text("""SELECT animal_id FROM animals_owned 
                                                            WHERE user_id = :user_id 
                                                               AND animal_id = :animal_id"""), 
                                                            [{"user_id": user_id, "animal_id": animal_id}]).fetchone().animal_id
                if animal_id_result is not None:
                    print("User owns animal, able to heal")
            except sqlalchemy.exc.NoResultFound:
                return "Unable to restock. You don't own an animal!"
            # find user's gold
            user = connection.execute(sqlalchemy.text("""SELECT SUM(gold) AS gold FROM 
                                                      transactions WHERE user_id = :user_id"""), 
                                                      [{"user_id": user_id}]).one()
            
            if gold < 0:
                return "Can't restore health with negative gold."

            health = 0
            if user.gold > gold:
                print("User has enough gold to restore health")
                health = gold * 2

            # find out how much health the animal has
            health_ani = connection.execute(sqlalchemy.text("SELECT SUM(health) FROM transactions WHERE animal_id = :animal_id"), {"animal_id": animal_id_result}).fetchone()[0]
            # cap max health at 100
            try:
                if health_ani + health >= 100:
                    health = abs(100 - health_ani)
            except TypeError:
                return "Unable to restock. You don't own an animal!"

            connection.execute(sqlalchemy.text("""INSERT INTO transactions (user_id, gold, animal_id, health, description) 
                                               VALUES (:user_id, -:gold, :animal_id, :health, :description)"""),
                                                 [{"user_id": user_id, "gold": gold, 
                                                   "animal_id": animal_id, "health": health, 
                                                   "description": "restore health"}])

    except IntegrityError or TypeError:
        return "restock: User not found"


    return f"restored {health} health with {gold} gold" # gold spent, health restored