from sqlite3 import IntegrityError
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
import time
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
    start = time.time()
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
            transaction_id = connection.execute(sqlalchemy.text("INSERT INTO transactions (user_id, description, gold) VALUES (:user_id, :description, :gold) RETURNING transaction_id"), 
                                            {"user_id": user_id, "description": description, "gold": -payment})
            

            enemy_row = connection.execute(sqlalchemy.text("""SELECT enemy_id, name, attack, defense 
                                                           FROM enemies ORDER BY RANDOM() LIMIT 1""")).fetchone()
            
            
            enemy_id = enemy_row.enemy_id
            enemy_name = enemy_row.name
            enemy_stats = {"attack": enemy_row.attack, "defense": enemy_row.defense}
            enemy_health = 100
            
            enemy_dialogue = {
                0: f" ate your {animal_name} and regurgitated it whole!!! RAA!",
                1: f" breathed fire on your {animal_name} 10 times!!! Beware of its owner, Angela.",
                2: f" wiggled its tail and casted a big wiggly wobbly spell on {animal_name}!",
                3: f" stomped on your {animal_name}'s foot!",
                4: f" screamed hysterically at {animal_name}!",
                5: f" performed water-breathing technique at your {animal_name}!",
                6: f" performed a spell and screamed 'ANGELATO!!' at {animal_name}!",
                7: f" yelled 'PERCELAY! AAAA' at {animal_name}!",
                8: f" threw a basektball at {animal_name} and yelled 'SRISH!'",
                9: f" created a loud noise towards {animal_name} and screamed 'I AM TAYLOR SRISH'",
                10: f" threw a SOFA on {animal_name}!!!!!!!",
                11: f" summoned hail on {animal_name} and screamed 'DALE GINGER ALE'!!",
                12: f" did the powerful floss, winked, and said 'SRISH TAUGHT ME' at {animal_name}!",
                13: f" did a princess Sophia spell on {animal_name} and sang, bursting your eardrums!",
                14: f" growled 'AUNTIE A' and created an earthquake where {animal_name} was standing!",
                15: f" casted the 'swish srish lala angela dale kale' spell on {animal_name}!"
            }
            
            user_dialogue = {
                0: f" fought back {enemy_name} fiercly with a stick!",
                1: f" grew in size to punch them {enemy_name} back!",
                2: f" defended itself from {enemy_name}!",
                3: f" created a magical ball of light towards {enemy_name}!",
                4: f" blasted a fireball at {enemy_name}.",
                5: f" danced around {enemy_name} to distract them.",
                6: f" slapped {enemy_name}!",
                7: f" threw a waterball at {enemy_name}!",
                8: f" created a tornado around {enemy_name}!"
            }
                        
            total_user_damage = 0
            total_enemy_damage = 0
            dialogue = ""
            if animal_name:
                for i in range(3):
                    # user dialogue
                    u_d = random.randint(0, 8)
                    dialogue += animal_name + user_dialogue[u_d] + " "
                    # enemy dialogue
                    e_d = random.randint(0, 15)
                    dialogue += enemy_name + enemy_dialogue[e_d] + " "
                    user_damage = random.randint(1, 10) - (attack - enemy_stats["defense"])
                    # min damage user can incur each round (out of 3) is 7
                    min_damage = 7
                    total_user_damage += max(min_damage, user_damage)
                    enemy_damage = random.randint(1, 10) - (enemy_stats["attack"] - defense)
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
    
    print("fight")
    end = time.time()
    print(str((end - start) * 1000) + " ms")
        
    return {
        "battle summary": f"{dialogue}",
        "animal used to fight": animal_name,
        "reward" : reward,
        "bonus"  : bonus,
        "enemy fought": enemy_name,
        "winner": winner
    }
