from sqlite3 import IntegrityError
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/barrels",
    tags=["barrels"],
    dependencies=[Depends(auth.get_api_key)],
)

class Barrel(BaseModel):
    sku: str

    ml_per_barrel: int
    potion_type: list[int]
    price: int

    quantity: int

@router.post("/deliver/{order_id}")
def post_deliver_barrels(barrels_delivered: list[Barrel], order_id: int):
    print(barrels_delivered)
    
    with db.engine.begin() as connection:
        try:
            # no need for potion keep track in mypotiontypes
            if barrels_delivered[0].sku == "SMALL_BLUE_BARREL" or barrels_delivered[0].sku == "MINI_BLUE_BARREL":
                connection.execute(sqlalchemy.text("INSERT INTO ledger (gold, potions, ml, potion_type, description) VALUES (-:gold, 0, :ml, 3, 'purchased small blue barrel')"), [{"gold": barrels_delivered[0].price, "ml": barrels_delivered[0].ml_per_barrel}])
            if barrels_delivered[0].sku == "SMALL_RED_BARREL" or barrels_delivered[0].sku == "MINI_RED_BARREL":
                connection.execute(sqlalchemy.text("INSERT INTO ledger (gold, potions, ml, potion_type, description) VALUES (-:gold, 0, :ml, 2, 'purchased small red barrel')"), [{"gold": barrels_delivered[0].price, "ml": barrels_delivered[0].ml_per_barrel}])
            if barrels_delivered[0].sku == "SMALL_GREEN_BARREL" or barrels_delivered[0].sku == "MINI_GREEN_BARREL":
                connection.execute(sqlalchemy.text("INSERT INTO ledger (gold, potions, ml, potion_type, description) VALUES (-:gold, 0, :ml, 1, 'purchased small green barrel')"), [{"gold": barrels_delivered[0].price, "ml": barrels_delivered[0].ml_per_barrel}])
            connection.execute(sqlalchemy.text("UPDATE global_inventory SET barrel_history = barrel_history + 1"))
        except IntegrityError:
            return "INTEGRITY ERROR!"
    
    print(f"barrels delivered: {barrels_delivered} order_id: {order_id}")

    return "OK"

# Gets called once a day
@router.post("/plan")
def get_wholesale_purchase_plan(wholesale_catalog: list[Barrel]):
    print(wholesale_catalog)
    # go through the wholesale catalog and check if you have enough gold
    with db.engine.begin() as connection:
        try:
            count = connection.execute(sqlalchemy.text("SELECT barrel_history FROM global_inventory"))
            gold = connection.execute(sqlalchemy.text("SELECT SUM(gold) FROM ledger"))
            gold = gold.fetchone()[0]
        except IntegrityError:
            return "INTEGRITY ERROR!"
        else:
            count = count.fetchone()[0]
            print(f"catalog at count {count} with modulo {count % 3}")
            
            if count % 3 == 1 and gold >= 100:
                return [
                    {
                        "sku": "SMALL_BLUE_BARREL",
                        "quantity": 1,
                    }
                ]
            elif count % 3 == 0 and gold >= 100:
                return [
                        {
                            "sku": "SMALL_RED_BARREL",
                            "quantity": 1,
                        }
                    ]
            elif count % 3 == 2 and gold >= 100:
                return [
                    {
                        "sku": "SMALL_GREEN_BARREL",
                        "quantity": 1,
                    }
                ]
            return []