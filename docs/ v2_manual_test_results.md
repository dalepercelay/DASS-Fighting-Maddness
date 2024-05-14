Made a create fighter function

create_fight(user_id:int, payment:int):

1.  curl -X 'POST' \
    'http://127.0.0.1:8000/fight/?user_id=24&payment=9' \
    -H 'accept: application/json' \
    -H 'access_token: dass' \
    -d ''
2.      { 
        "reward": 10,
        "bonus": 90
        }
