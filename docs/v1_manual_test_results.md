**Example Workflow #1**:

Loli Boppi Gameplay:

We will make a pro boxer named Loli Boppi. We start off by calling POST /create-user/Loli-Boppi, and we get back her user id. Loli Boppi comes into our shop, asking to buy an animal for a fight. She starts off by getting a catalog of the animals by calling a GET /catalog. Loli Boppi comes in with 200 gold, and let’s say she was interested in an animal named Feefee that cost 70 gold. She then calls POST /buy-animal/Feefee. She is then charged 70 gold and is left with 130 gold and Feefee afterwards.

Create User

1. curl -X 'POST' \
   'http://127.0.0.1:8000/user/create-user?name=Loli%20Boppi' \
   -H 'accept: application/json' \
   -H 'access_token: dass' \
   -d ''
2. "Successfully created a user: 12"

Get Catalog

1. curl -X 'GET' \
   'http://127.0.0.1:8000/catalog' \
   -H 'accept: application/json'
2. [
   {
   "id": 3,
   "name": "FeeFee",
   "attack": 30,
   "defense": 40,
   "price": 70
   }
   ]

Buy Animal

1. curl -X 'POST' \
   'http://127.0.0.1:8000/animal/buy-animal/FeeFee?animal_id=3&user_id=12&user_name=Loli%20Boppi' \
   -H 'accept: application/json' \
   -H 'access_token: dass' \
   -d ''
2. {
   "delivery_status": true
   }
