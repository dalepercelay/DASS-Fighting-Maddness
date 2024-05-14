from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.post("/reset")
def reset():    
    with db.engine.begin() as connection:
        sql = ""
        # reset tables
        sql += "TRUNCATE TABLE fights, enemies, animals, users, transactions;"
        # pre-insert 2 animals
        sql += "INSERT INTO animals (animal_id, name, attack, defense, price) VALUES (1, 'FeeFee', 45, 30, 40);INSERT INTO animals (animal_id, name, attack, defense, price) VALUES (2, 'Kiwi', 50, 40, 60);"
        # pre-insert 5 enemies
        sql += "INSERT INTO enemies (name, attack, defense) VALUES ('Gollum', 60, 15);INSERT INTO enemies (name, attack, defense) VALUES ('FEELTH', 37, 56);INSERT INTO enemies (name, attack, defense) VALUES ('GARY', 73, 20);INSERT INTO enemies (name, attack, defense) VALUES ('MiniMooBAMBA', 20, 70);INSERT INTO enemies (name, attack, defense) VALUES ('Mid', 50, 50);"
        # update their healths in transactions
        sql += "INSERT INTO transactions (description, animal_id, health) VALUES ('created animal FeeFee', 1, 100);INSERT INTO transactions (description, animal_id, health) VALUES ('created animal Kiwi', 2, 100)"
        connection.execute(sqlalchemy.text(sql))

    return "OK"

