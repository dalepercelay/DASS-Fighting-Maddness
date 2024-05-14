Made a create fighter function

We will make a fighting scene, where will create the fight using a player, say Ash Ketchum. He will randomly be thrown against an opponent, and will have to fight using his special animal. If he wins, he get paid 10 times the amount he paid, plus a 10 gold reward. If he loses, he get 0. 


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
