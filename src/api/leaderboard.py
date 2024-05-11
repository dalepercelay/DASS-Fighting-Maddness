from sqlite3 import IntegrityError
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/leaderboard",
    tags=["leaderboard"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.get("/")
def leaderboard():
    # TODO:
    # get a list of users join on transactions table order by SUM(gold) -> can't use aggregate functions
    # at end of SQL statement so figure it out by windowing?

    # also use the row_number to figure out ties -> up to you how to implement
    return "OK" # a list of users in the leaderboard order