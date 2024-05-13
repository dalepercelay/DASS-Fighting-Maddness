from sqlite3 import IntegrityError
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/fight",
    tags=["fight"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.post("/")
def create_fight(user_id: int, entry_fee: int):
    # TODO
    # find out if they have an animal associated with them to start a fight (if not, exit)

    # insert into transactions the user_id and gold spent for the entry fee, description = "enter fight"

    # randomly assign an enemy

    # calculate the fight results

    # if win, calculate the bonus they get from their entry fee

    # else just add a fixed amount of gold for winning

    # if lose, decrease health of animal
    # if health of animal <= 0, set user_id of that animal to null (available again) and reset health to 100
    # make sure to also remove animal_id from user (set to null)

    # insert into transactions the user_id and gold won/health lost depending on outcome
    # description is "fight + {outcome: won/lost}""
    # return transaction id from this query to user in the insert into fights statement below

    # insert into fights user_id, animal_id, enemy_id, outcome

    return "OK" # fight outcome, gold and health change

# @router.get("/result")
# def fight_result():
#     # should be implemented in create-fight --> not two separate functions
#     return "OK"