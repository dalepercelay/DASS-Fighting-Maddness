from sqlite3 import IntegrityError
from fastapi import APIRouter
import sqlalchemy
from src import database as db

router = APIRouter()
@router.get("/catalog", tags=["catalog"])
def get_catalog():
    '''Get catalog of all available animals.'''
    try:
        # return the list of all available animals in the catalog
        mylist = []
        with db.engine.begin() as connection:
            animals = connection.execute(sqlalchemy.text("SELECT animal_id, name, attack, defense, price FROM animals WHERE in_use IS FALSE"))
            for animal in animals.fetchall():
                mylist.append(
                    {
                        "id": animal.animal_id,
                        "name": animal.name,
                        "attack": animal.attack,
                        "defense": animal.defense,
                        "price": animal.price,
                    }
        )
    except IntegrityError:
        return "catalog: INTEGRITY ERROR!"

    return mylist