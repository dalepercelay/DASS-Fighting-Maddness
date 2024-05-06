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


# Gets called once a day
@router.post("/plan")
def get_capacity_plan():
    """ 
    Start with 1 capacity for 50 potions and 1 capacity for 10000 ml of potion. Each additional 
    capacity unit costs 1000 gold.
    """
    
    try:
        with db.engine.begin() as connection:
            print("hi")
    except IntegrityError:
        return "INTEGRITY ERROR!"
    return {
        "potion_capacity": 0,
        "ml_capacity": 0
    }

class CapacityPurchase(BaseModel):
    potion_capacity: int
    ml_capacity: int

# Gets called once a day
@router.post("/deliver/{order_id}")
def deliver_capacity_plan(capacity_purchase : CapacityPurchase, order_id: int):
    """ 
    Start with 1 capacity for 50 potions and 1 capacity for 10000 ml of potion. Each additional 
    capacity unit costs 1000 gold.
    """
    try:
        with db.engine.begin() as connection:
            print("hi")
    except IntegrityError:
        return "INTEGRITY ERROR!"
    return "Successfully delivered capacity plan"
