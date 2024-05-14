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

@router.post("/")
def create_fight(user_id:int, payment:int):
    with db.engine.begin() as connection:
        # make sure user has an animal before fighting
        animal_id = connection.execute(sqlalchemy.text("SELECT COALESCE(animal_id, -1) FROM users WHERE user_id = :user_id"), {"user_id": user_id})
        
        if animal_id.fetchone()[0] == -1:
            return "Cannot fight because you don't have an animal! Buy one at the shop!"
        
        sql_query = """SELECT a.name, u.name, a.attack, a.defense, a.health FROM users u
                    JOIN animals a ON u.animal_id = a.animal_id AND u.user_id = a.user_id
                     WHERE u.user_id = :user_id"""
        animal_name, username, attack, defense, health = connection.execute(sqlalchemy.text(sql_query), {"user_id":user_id}).fetchone()
        
        # make sure animal health isn't less than 10!
        animal_health = connection.execute(sqlalchemy.text("SELECT SUM(health) FROM transactions WHERE animal_id = :animal_id"), {"animal_id": animal_id})
        if animal_health.fetchone()[0] <= 10:
            # make user lose the animal
            connection.execute(sqlalchemy.text("UPDATE animals SET user_id = NULL WHERE user_id = :user_id; UPDATE users SET animal_id = NULL WHERE user_id = :user_id"), [{"user_id": user_id}])
            return "Cannot fight! Animal is too injured! Buy another one at the shop!"
        
        loser = False
        bonus = 0
        reward = 0
        description = "FIGHT!"
        transaction_id = connection.execute(sqlalchemy.text("INSERT INTO transactions (description,gold)"
                                           "VALUES (:description, :gold) RETURNING transaction_id"), {"description": description, "gold": -payment})
        enemy_result = connection.execute(sqlalchemy.text("SELECT * FROM Enemies ORDER BY RANDOM() LIMIT 1"))
        enemy_row = enemy_result.fetchone()
        enemy_id = enemy_row[0]
        enemy_name = enemy_row[2]
        enemy_stats = {"attack": enemy_row[4], "defense": enemy_row[5]}
        enemy_health = enemy_row[3]
        
        total_user_damage = 0
        total_enemy_damage = 0
        if animal_name:
            for i in range(3):
               user_damage = random.randint(1, 50) - (attack - enemy_stats["defense"])
               total_user_damage += max(7, user_damage)
               enemy_damage = random.randint(1, 35) - (enemy_stats["attack"] - defense)
               total_enemy_damage += max(7, enemy_damage)
               if health-total_user_damage <= 0 or enemy_health-total_enemy_damage <= 0:
                     break

        health -= total_user_damage
        enemy_health -= total_enemy_damage
        if enemy_health>health:
            winner = enemy_name  
            loser = True
        else:
            winner = username
        if loser == False:
            bonus = 10*payment
            reward = 10
            
        # insert into the fight table
        transaction_id = transaction_id.fetchone()[0]
        outcome = winner + " won!"
        connection.execute(sqlalchemy.text("INSERT INTO fights (outcome, animal_id, user_id, enemy_id, transaction_id) VALUES (:outcome, :animal_id, :user_id, :enemy_id, :transaction_id)"), {"outcome": outcome, "enemy_id": enemy_id, "animal_id": animal_id, "user_id": user_id, "transaction_id": transaction_id})
           
        # update transactions table for result 
        result_sql = "INSERT INTO transactions (user_id, gold, description, animal_id) VALUES (:user_id, :gold, :description, :animal_id);"
        # update animal health
        result_sql += "INSERT INTO transactions (description, animal_id, health) VALUES ('animal injury after fight', :animal_id, -:health)"
        connection.execute(sqlalchemy.text(result_sql), {"health": total_user_damage, "animal_id": animal_id, "user_id": user_id, "description": "fight result", "gold": bonus + reward})
        
    return {
        "reward" : reward,
        "bonus"  : bonus,
        "enemy fought": enemy_name,
        "winner": winner
    }