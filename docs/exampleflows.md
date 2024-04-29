Technical Flows

Example 1:

Loli Boppi Gameplay:

We will make a pro boxer named Loli Boppi. We start off by calling POST /create-user/Loli-Boppi, and we get back her user id. Loli Boppi comes into our shop, asking to buy an animal for a fight. She starts off by getting a catalog of the animals by calling a GET /catalog. Loli Boppi comes in with 200 gold, and let’s say she was interested in an animal named Feefee that cost 70 gold. She then calls POST /buy-animal/Feefee. She is then charged 70 gold and is left with 130 gold and Feefee afterwards.

Example 2:

Ash Ketchum’s Gameplay:

Ash starts by creating his account using: POST ‘/create-user/Ash-Ketchum’ This sets his profile up with 200 gold and 100 health.

He then looks through the catalog with GET ‘/catalog/’ to view all the available animals, and chooses a monkey for 65 gold. He calls POST ‘/buy-animal/Monkey’, and he is left with 135 gold.

He wants to fight, and uses POST ‘/fight/’ with { "user_id": Ash’s user ID, "animal-use": true, "payment": 10 } He now has 125 gold.

Afterwards, he uses GET ‘/fight-result/’ to find out he won the fight, earning him 110 gold (100 gold bonus plus 10 gold victory reward). He now has 235 gold.

Example 3:

Steve Irwin’s Gameplay:

Steve starts by creating his account using: POST ‘/create-user/Steve-Irwin’ This sets his profile up with 200 gold and 100 health.

He then looks through the catalog with GET ‘/catalog/’ to view all the available animals, and chooses an alligator for 140 gold. He calls POST ‘/buy-animal/, and he is left with 60 gold.

He wants to fight, and uses POST ‘/fight/’ with { "user_id": Irwin, "animal-use": true, "payment": 50 }

He loses, and now has 10 gold.

To recover, Steve uses POST ‘/restock/’ to spend 5 gold for 10 health points, and he's got just 5 gold left. He wants to know his standings, so uses GET ‘/leaderboard/’ to see he is in last place.
