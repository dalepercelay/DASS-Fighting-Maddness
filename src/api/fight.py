from sqlite3 import IntegrityError
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db
import random
router = APIRouter(
    prefix="/fight",
    tags=["fight"],
    dependencies=[Depends(auth.get_api_key)],
)

# can now pick whichever animal to fight
@router.post("")
def create_fight(user_id: int, animal_id: int, payment:int):
    '''Create a fight. If won, reward of 10 gold plus bonus of specified payment * 10. 
    If fight lost, gold paid is lost as well. Animal can lose health during a fight'''

    try:
        with db.engine.begin() as connection:
            # make sure payment isn't a negative number
            if payment <= 0:
                return "Cannot accept your payment."
            
            # make sure the animal and user ids exist
            try:
                username = connection.execute(sqlalchemy.text("SELECT name FROM users WHERE user_id = :user_id"), 
                                      [{"user_id": user_id}]).fetchone()[0]
                connection.execute(sqlalchemy.text("SELECT name FROM animals WHERE animal_id = :animal_id"), 
                                      [{"animal_id": animal_id}]).fetchone()[0]
                # check to make sure it's owned by the right user
                check = connection.execute(sqlalchemy.text("SELECT user_id FROM animals_owned WHERE animal_id = :animal_id"), {"animal_id": animal_id}).fetchone()[0]
                if check != user_id:
                    return "Animal isn't owned by you so you cannot fight with that animal. >:C"
            except TypeError:
                return "The IDs you provided don't exist"
            animal_name, attack, defense = connection.execute(sqlalchemy.text("SELECT name, attack, defense FROM animals WHERE animal_id = :animal_id"), {"animal_id": animal_id}).fetchone()
            health = connection.execute(sqlalchemy.text("SELECT SUM(health) FROM transactions WHERE animal_id = :animal_id"), {"animal_id": animal_id}).fetchone()[0]
            animal_h = health
            print('animal health is' + str(animal_h) + " " + str(animal_id))
            # make sure animal health isn't less than 10!
            if animal_h <= 10:
                return "Cannot fight! Animal is too injured! Restock its health at the store!"
            
            loser = False
            bonus = 0
            reward = 0
            description = "FIGHT!"
            transaction_id = connection.execute(sqlalchemy.text("INSERT INTO transactions (user_id, description, gold)"
                                            "VALUES (:user_id, :description, :gold) RETURNING transaction_id"), 
                                            {"user_id": user_id, "description": description, "gold": -payment})
            enemy_row = connection.execute(sqlalchemy.text("""SELECT enemy_id, name, attack, defense 
                                                           FROM enemies ORDER BY RANDOM() LIMIT 1""")).fetchone()
            enemy_id = enemy_row.enemy_id
            enemy_name = enemy_row.name
            enemy_stats = {"attack": enemy_row.attack, "defense": enemy_row.defense}
            enemy_health = 100
            
            total_user_damage = 0
            total_enemy_damage = 0
            if animal_name:
                for i in range(3):
                    user_damage = random.randint(1, 50) - (attack - enemy_stats["defense"])
                    # min damage user can incur each round (out of 3) is 7
                    min_damage = 7
                    total_user_damage += max(min_damage, user_damage)
                    enemy_damage = random.randint(1, 35) - (enemy_stats["attack"] - defense)
                    # min damage enemy can incur each round (out of 3) is 7
                    total_enemy_damage += max(min_damage, enemy_damage)
                    if health-total_user_damage <= 0 or enemy_health-total_enemy_damage <= 0:
                        # one of them died
                        break

            health -= total_user_damage
            enemy_health -= total_enemy_damage
            # even if there is a tie, as long as the user has more or equal health than enemy, then they would be declared as the winner
            if enemy_health>health:
                winner = enemy_name  
                # outcome is bool false when enemy wins
                outcome = False
                loser = True
            else:
                # outcome is bool true when user wins
                outcome = True
                winner = username
            if loser == False:
                reward = 10 # regular reward is 10
                bonus = reward*payment # if bet gold (in payment), and won, also get base reward * paid gold

                
            # insert into the fight table
            transaction_id = transaction_id.fetchone()[0]
            connection.execute(sqlalchemy.text("""INSERT INTO fights (outcome, animal_id, user_id, enemy_id, transaction_id) 
                                               VALUES (:outcome, :animal_id, :user_id, :enemy_id, :transaction_id);"""), 
                               {"outcome": outcome, "enemy_id": enemy_id, "animal_id": animal_id, "user_id": user_id, "transaction_id": transaction_id})
            
            # update transactions table for result 
            result_sql = """INSERT INTO transactions (user_id, gold, description, animal_id) 
            VALUES (:user_id, :gold, :description, :animal_id);"""
            # always make sure animal health can only go down to 0 minimum
            if animal_h - total_user_damage <= 0:
                total_user_damage = animal_h
            result_sql += "INSERT INTO transactions (description, animal_id, health) VALUES ('animal injury after fight', :animal_id, -:health);"
            connection.execute(sqlalchemy.text(result_sql), 
                               {"health": total_user_damage, "animal_id": animal_id, "user_id": user_id, "description": "fight result", "gold": bonus + reward})

    except IntegrityError:
        return "create fight: INTEGRITY ERROR!"
        
    return {
        "animal used to fight": animal_name,
        "reward" : reward,
        "bonus"  : bonus,
        "enemy fought": enemy_name,
        "winner": winner
    }
