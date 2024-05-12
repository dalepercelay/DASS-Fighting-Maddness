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
        sql += "TRUNCATE TABLE fights, animals, users, transactions;"
        # pre-insert 2 animals
        sql += "INSERT INTO animals (name, attack, defense, price) VALUES ('FeeFee', 45, 30, 40);INSERT INTO animals (name, attack, defense, price) VALUES ('Kiwi', 50, 40, 60);"
        connection.execute(sqlalchemy.text(sql))

    return "OK"

