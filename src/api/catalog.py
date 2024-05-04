from sqlite3 import IntegrityError
from fastapi import APIRouter
import sqlalchemy
from src import database as db

router = APIRouter()
# added yeeLOW information
@router.get("/catalog/", tags=["catalog"])
def get_catalog():
    try:
        with db.engine.begin() as connection:
            red = connection.execute(sqlalchemy.text("SELECT id, name, cost, red, green, blue, dark FROM mypotiontypes WHERE name = 'RARA_RED'"))
            blue = connection.execute(sqlalchemy.text("SELECT id, name, cost, red, green, blue, dark FROM mypotiontypes WHERE name = 'bluey_mooey'"))    
            green = connection.execute(sqlalchemy.text("SELECT id, name, cost, red, green, blue, dark FROM mypotiontypes WHERE name = 'GOOGOOGREEN'"))
            purple = connection.execute(sqlalchemy.text("SELECT id, name, cost, red, green, blue, dark FROM mypotiontypes WHERE name = 'burple'"))
            yellow = connection.execute(sqlalchemy.text("SELECT id, name, cost, red, green, blue, dark FROM mypotiontypes WHERE name = 'yeeLOW'"))
            green_p = connection.execute(sqlalchemy.text("SELECT SUM(potions) FROM ledger WHERE potion_type = 1"))
            red_p = connection.execute(sqlalchemy.text("SELECT SUM(potions) FROM ledger WHERE potion_type = 2"))
            blue_p = connection.execute(sqlalchemy.text("SELECT SUM(potions) FROM ledger WHERE potion_type = 3"))
            purple_p = connection.execute(sqlalchemy.text("SELECT SUM(potions) FROM ledger WHERE potion_type = 4"))
            yellow_p = connection.execute(sqlalchemy.text("SELECT SUM(potions) FROM ledger WHERE potion_type = 5"))
    except IntegrityError:
        return "INTEGRITY ERROR!"
    """
    Each unique item combination must have only a single price.
    """
    
    # change this
    mylist = []
    blue = blue.fetchone()
    blue_p = blue_p.fetchone()[0]
    if  blue_p is not None and blue_p > 0:
        mylist.append({
                    "sku": blue[1],
                    "name": blue[1],
                    "quantity": 1,
                    "price": blue[2],
                    "potion_type": [blue[3], blue[4], blue[5], blue[6]],
                }
            )
    red = red.fetchone()
    red_p = red_p.fetchone()[0]
    if  red_p is not None and red_p > 0:
        mylist.append(
                {
                    "sku": red[1],
                    "name": red[1],
                    "quantity": 1,
                    "price": red[2],
                    "potion_type": [red[3], red[4], red[5], red[6]],
                }
        )
    yellow = yellow.fetchone()
    yellow_p = yellow_p.fetchone()[0]
    if  yellow_p is not None and yellow_p > 0:
        mylist.append(
                {
                    "sku": yellow[1],
                    "name": yellow[1],
                    "quantity": 1,
                    "price": yellow[2],
                    "potion_type": [yellow[3], yellow[4], yellow[5], yellow[6]],
                }
        )
    green = green.fetchone()
    green_p = green_p.fetchone()[0]
    if green_p is not None and green_p > 0:
        mylist.append(
                {
                    "sku": green[1],
                    "name": green[1],
                    "quantity": 1,
                    "price": green[2],
                    "potion_type": [green[3], green[4], green[5], green[6]],
                }
        )
    purple = purple.fetchone()
    purple_p = purple_p.fetchone()[0]
    if  purple_p is not None and purple_p > 0:
        mylist.append(
                {
                    "sku": purple[1],
                    "name": purple[1],
                    "quantity": 1,
                    "price": purple[2],
                    "potion_type": [purple[3], purple[4], purple[5], purple[6]],
                }
        )
    return mylist