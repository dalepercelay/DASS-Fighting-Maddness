
We will make a fighting scene, where will create the fight using a player, say Ash Ketchum. He will randomly be thrown against an opponent, and will have to fight using his special animal. If he wins, he get paid 10 times the amount he paid, plus a 10 gold reward. If he loses, he get 0. 

Create user
1.  curl -X 'POST' \
  'http://127.0.0.1:8000/user/create-user?name=Ash' \
  -H 'accept: application/json' \
  -H 'access_token: dass' \
  -d ''
2.  "Successfully created a user: 26"

Create Animal
1.  curl -X 'POST' \
  'http://127.0.0.1:8000/animal/create-animal/{name}?animal_name=PothePanda&attack=80&defense=90' \
  -H 'accept: application/json' \
  -H 'access_token: dass' \
  -d ''
2.  "created animal id 12: PothePanda, 80, 90"

Buy Animal
1.  curl -X 'POST' \
  'http://127.0.0.1:8000/animal/buy-animal/PothePanda?animal_id=12&user_id=26' \
  -H 'accept: application/json' \
  -H 'access_token: dass' \
  -d ''
2.  {
  "delivery_status": true
}


create_fight(user_id:int, payment:int):

1.  curl -X 'POST' \
  'http://127.0.0.1:8000/fight/?user_id=26&payment=10' \
  -H 'accept: application/json' \
  -H 'access_token: dass' \
  -d ''
2.     {
  "reward": 10,
  "bonus": 100
}

