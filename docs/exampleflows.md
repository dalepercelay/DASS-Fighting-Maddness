Technical Flows

Example 1:

Loli Boppi Gameplay:

We will make a pro boxer named Loli Boppi. We start off by calling POST /create-user/Loli-Boppi, and we get back her user id. Loli Boppi comes into our shop, asking to buy an animal for a fight. She starts off by getting a catalog of the animals by calling a GET /catalog. Loli Boppi comes in with 200 gold, and let’s say she was interested in an animal named Feefee that cost 40 gold. She then calls POST /buy-animal/Feefee. She is then charged 40 gold and is left with 130 gold and Feefee afterwards.

Example 2:

Ash Ketchum’s Gameplay:

Ash starts by creating his account using: POST ‘/create-user/Ash-Ketchum’ This sets his profile up with 200 gold.

He then looks through the catalog with GET ‘/catalog/’ to view all the available animals, and chooses a PothePanda for 170 gold. He calls POST ‘/buy-animal/PothePanda, and he is left with 30 gold.

He wants to fight, and uses POST ‘/fight/’ with { "user_id": Ash’s user ID, "payment": 10 } so then he is left with 125 gold. But after he fights, assume he won, earning him 110 gold (100 gold bonus plus 10 gold victory reward). He now has 140 gold.

He restocks his animal's health by calling GET '/inventory/restock'  with { "user_id": Ash’s user ID, "gold": 30 }. He is then left with 110 gold. He finally calls GET '/leaderboard' to see his rankings

Example 3:

Steve Irwin’s Gameplay:

Steve starts by creating his account using: POST ‘/create-user/Steve-Irwin’ This sets his profile up with 200 gold.

He then looks through the catalog with GET ‘/catalog/’ to view all the available animals, and chooses Kiwi for 60 gold. He is now left with 140 gold.

He wants to fight, and uses POST ‘/fight/’ with { "user_id": Irwin's id, "payment": 50 }

He loses, and now has 90 gold based on his GET '/inventory' call
