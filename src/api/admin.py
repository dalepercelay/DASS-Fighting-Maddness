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
    """
    Reset the game state. Gold goes to 100, all potions are removed from
    inventory, and all barrels are removed from inventory. Carts are all reset.
    """
    
    # used truncate table [] instead of delete from []
    
    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("UPDATE global_inventory SET barrel_history = 0, potion_history = 0"))
        connection.execute(sqlalchemy.text("TRUNCATE TABLE ledger"))
        connection.execute(sqlalchemy.text("TRUNCATE TABLE cart_items"))
        connection.execute(sqlalchemy.text("TRUNCATE TABLE carts"))
        connection.execute(sqlalchemy.text("INSERT INTO ledger (gold, description) VALUES (100, 'reset')"))

    return "OK"

