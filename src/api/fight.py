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
        description = "Bought animal"
        connection.execute(sqlalchemy.text("INSERT INTO transactions (description,gold)"
                                           "VALUES (:description, :gold)"), {"description": description, "gold": -payment})
        enemy_result = connection.execute(sqlalchemy.text("SELECT * FROM Enemies ORDER BY RANDOM() LIMIT 1"))
        enemy_row = enemy_result.fetchone()
        enemy_name = enemy_row[0]
        enemy_stats = {"attack": enemy_row[4], "defense": enemy_row[5]}
        enemy_health = enemy_row[3]
        sql_query = """SELECT a.name, u.name, a.attack, a.defense, a.health FROM users u
                     LEFT JOIN animals a ON u.animal_id = a.animal_id AND u.user_id = a.user_id
                     WHERE u.user_id = :user_id"""
        animal_name, username, attack, defense, health = connection.execute(sqlalchemy.text(sql_query), {"user_id":user_id, "animalUse":animalUse}).fetchone()
        total_user_damage =0
        total_enemy_damage = 0
        winner = False
        if animal_name:
            for i in range(3):
               user_damage = random.randint(1, 35) - (attack - enemy_stats["defense"])
               total_user_damage += max(0, user_damage)
               enemy_damage = random.randint(1, 35) - (enemy_stats["attack"] - defense)
               total_enemy_damage += max(0, enemy_damage)
               if health-total_user_damage <= 0 or enemy_health-total_enemy_damage <= 0:
                     break

        health -= total_user_damage
        enemy_health -= total_enemy_damage
        if enemy_health>health:
            winner = enemy_name  
        else:
            winner = username
        




    return "OK"

            


   

@router.get("/result")
def fight_result():
    return "OK"