# 2nd Example Workflow

Ash Ketchum’s Gameplay:

Ash starts by creating his account using: POST ‘/create-user/Ash-Ketchum’ This sets his profile up with 200 gold.

He then looks through the catalog with GET ‘/catalog/’ to view all the available animals, and chooses a PothePanda for 170 gold. He calls POST ‘/buy-animal/PothePanda, and he is left with 30 gold.

He wants to fight, and uses POST ‘/fight/’ with { "user_id": Ash’s user ID, "payment": 10 } so then he is left with 125 gold. But after he fights, assume he won, earning him 110 gold (100 gold bonus plus 10 gold victory reward). He now has 140 gold.

He restocks his animal's health by calling GET '/inventory/restock'  with { "user_id": Ash’s user ID, "gold": 30 }. He is then left with 110 gold. He finally calls GET '/leaderboard' to see his rankings

Create user
1.  curl -X 'POST' \
  'http://127.0.0.1:8000/user/create-user?name=Ash' \
  -H 'accept: application/json' \
  -H 'access_token: dass' \
  -d ''
2.  "Successfully created a user: 28"

Get inventory audit
1. curl -X 'GET' \
  'http://127.0.0.1:8000/inventory/audit?user_id=28' \
  -H 'accept: application/json' \
  -H 'access_token: dass'
2. {
      "gold": 200,
      "animal": -1,
      "animal health": null
    }

Create Animal
1.  curl -X 'POST' \
  'http://127.0.0.1:8000/animal/create-animal/{name}?animal_name=PothePanda&attack=80&defense=90' \
  -H 'accept: application/json' \
  -H 'access_token: dass' \
  -d ''
2. "created animal id 13: PothePanda, 80, 90"

Buy Animal
1. curl -X 'POST' \
  'http://127.0.0.1:8000/animal/buy-animal/PothePanda?animal_id=13&user_id=28' \
  -H 'accept: application/json' \
  -H 'access_token: dass' \
  -d ''
2.  {
  "delivery_status": true
}

Create a Fight

1. curl -X 'POST' \
  'http://127.0.0.1:8000/fight/?user_id=28&payment=10' \
  -H 'accept: application/json' \
  -H 'access_token: dass' \
  -d ''
2. {
      "reward": 10,
      "bonus": 100,
      "enemy fought": "Gollum",
      "winner": "Ash"
    }

Restock
1. curl -X 'GET' \
  'http://127.0.0.1:8000/inventory/restock?user_id=28&gold=30' \
  -H 'accept: application/json' \
  -H 'access_token: dass'
2. "restored 60 health with 30 gold"

Leaderboard
1. curl -X 'GET' \
  'http://127.0.0.1:8000/leaderboard/' \
  -H 'accept: application/json' \
  -H 'access_token: dass'

2. [
      {
        "name": "Loli Boppi",
        "gold": 160
      },
      {
        "name": "Ash",
        "gold": 110
      }
    ]

# 3rd Example Workflow

Steve Irwin’s Gameplay:

Steve starts by creating his account using: POST ‘/create-user/Steve-Irwin’ This sets his profile up with 200 gold.

He then looks through the catalog with GET ‘/catalog/’ to view all the available animals, and chooses Kiwi for 60 gold. He is now left with 140 gold.

He wants to fight, and uses POST ‘/fight/’ with { "user_id": Irwin's id, "payment": 50 }

He loses, and now has 90 gold based on his GET '/inventory' call

Create user
1. curl -X 'POST' \
  'http://127.0.0.1:8000/user/create-user?name=Steve%20Irwin' \
  -H 'accept: application/json' \
  -H 'access_token: dass' \
  -d ''
2. "Successfully created a user: 30"

Get catalog
1. curl -X 'GET' \
  'http://127.0.0.1:8000/catalog' \
  -H 'accept: application/json'
2. [
    {
      "id": 2,
      "name": "Kiwi",
      "attack": 50,
      "defense": 40,
      "price": 60
    }
  ]

Buys animal
1. curl -X 'POST' \
  'http://127.0.0.1:8000/animal/buy-animal/Kiwi?animal_id=2&user_id=30' \
  -H 'accept: application/json' \
  -H 'access_token: dass' \
  -d ''
2.  {
      "delivery_status": true
    }

Create a fight
1. curl -X 'POST' \
  'http://127.0.0.1:8000/fight/?user_id=30&payment=50' \
  -H 'accept: application/json' \
  -H 'access_token: dass' \
  -d ''
2. {
    "reward": 0,
    "bonus": 0,
    "enemy fought": "MiniMooBAMBA",
    "winner": "MiniMooBAMBA"
  }

Get inventory
1. curl -X 'GET' \
  'http://127.0.0.1:8000/inventory/audit?user_id=30' \
  -H 'accept: application/json' \
  -H 'access_token: dass'
2. {
    "gold": 90,
    "animal": "Kiwi",
    "animal health": 0
  }