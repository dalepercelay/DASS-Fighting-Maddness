**Example Workflow #1**:

Loli Boppi Gameplay:

We will make a pro boxer named Loli Boppi. We start off by calling POST /create-user/Loli-Boppi, and we get back her user id. Loli Boppi comes into our shop, asking to buy an animal for a fight. She starts off by getting a catalog of the animals by calling a GET /catalog. Loli Boppi comes in with 200 gold, and let’s say she was interested in an animal named Feefee that cost 70 gold. She then calls POST /buy-animal/Feefee. She is then charged 70 gold and is left with 130 gold and Feefee afterwards.

**Testing Results:**

