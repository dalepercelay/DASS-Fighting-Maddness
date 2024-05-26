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
    '''Returns a list of all users ranked by gold.'''
    try:
        with db.engine.begin() as connection:
            users = connection.execute(sqlalchemy.text("""SELECT users.name AS username, SUM(transactions.gold) AS gold 
                                                            FROM users
                                                            JOIN transactions ON users.user_id = transactions.user_id
                                                            GROUP BY users.name
                                                            ORDER BY gold DESC;""")).fetchall()
    except IntegrityError:
        return "leaderboard: INTEGRITY ERROR!"
    
    return [{"name": user.username, "gold": user.gold} for user in users]