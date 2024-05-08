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
def get_inventory():
    # query in the actual data
    try:
        with db.engine.begin() as connection:
            print("hi")
    except IntegrityError:
        return "INTEGRITY ERROR!"
    return {"number_of_potions": 1, "ml_in_barrels": 1, "gold": 1}

@router.get("/restock")
def get_inventory():
    return "OK"