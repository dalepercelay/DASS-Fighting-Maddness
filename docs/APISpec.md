API Specification for Group Project:

List of API calls:
Get Catalog of Animals (all animals available to be bought)
Create an Animal (user can create an animal to catalog and get money that way)
Create User (id, name, gold, animal, health status for user)
Buy an Animal (for one fight at a time)
Create a Fight (pay 10 gold to fight, gets 0 - 100 chance of winning – higher if higher stats)
Fight Result Update (get money if win, lose health)
Leaderboard (after every fight result updates, the leaderboard updates)
Restock on Resources (buying health)

Get Catalog of Animals - GET Method (/catalog/)
Description: Gets a catalog of all the animals available for purchase. Only one user can have an animal at a time - when they get the animal, it is removed from catalog.
Response:
{ 
	“id”: “integer”
	“name”: “string”
	“stats”: “integer” /* between 1 and 100 */
	“price”: “integer” 
}

Create an Animal - POST Method (/create-animal/{name})
Description: Users can create animals (with given name, stats, price - we create id) and it can be considered an investment. It will take 100 gold for users to create an animal, but once they sell it to the main store, they can sell it for 50 no matter what animal it is. But then the users can create a price to sell their animals for in the catalog. 
Request:
{
“name”: “string”
“defense”: “integer” /* between 1 and 50 */
"attack": "integer" /* between 1 and 50 */
“price”: “integer”
}
Response:
{
	“success”: “boolean”
}

Create User - POST Method (/create-user/{name})
Description: Given a name, create a user which has starting gold 200, no animal, 100 health status (from 0 - 100) for the user.
Request:
{
	“name”: “string”
}
Response:
{
	“user_id”: “integer”
}

Buy an Animal - POST Method (/buy-animal/{name})
Description: Given an animal id from the catalog, buy an animal (if the user has enough gold). Return if delivery was successful (user had enough gold to buy).
(An animal starts with 100 health. If their health gets to 0, they cannot be used by the user anymore)
Request: 
{
	“name”: “string”
]}
Response:
{
	“delivery-status”: “boolean”
}

Create a Fight - POST Method (/fight/)
Description: Everyday, there will be one main fight/battle. Users will pay 0 - 10 gold in order to participate in the fight.  
Request:
{
	“user_id”: “integer”
	“animal-use”: “boolean” /* true if using their animal */
	“payment”: “integer” /* between 1 - 10 */
}

Response:
{
	“success”: “boolean”
}


Fight Result Update - GET Method (/fight-result/)
Description: Winning the fight would allow them to earn money based on how much they choose to bet their gold by 10. For example, if a user bet 10 gold and won the battle, then they can get 100 gold total from the battle (aka bonus) plus 10 gold as a congratulations reward. If they lose the fight though, they just lose the gold they originally bet in the first place. Furthermore, if they lose, their animal' health is decreased by 20. 
Response:
{
	“reward”: “integer” 10 (if they win) or 0 (if they lose),
	“bonus”: “integer” (amount of gold user bet) * 10 (if they win) or 0 (if they lose)
}

Leaderboard - GET Method (/leaderboard/)
Description: Everyday, the leaderboard would be updated based on the rankings of users with the highest amount of gold
Response: /* ordered by number of gold */
{
	“name”: “string” /* user name */
	“gold”: “string” /* how much gold the user has */
}

Restock on Resources - POST Method (/restock/)
Description: After every fight/battle, the user will need to purchase gold to restock their health accordingly. They will purchase 10 gold for 20 health, 20 gold for 40 health, and 30 gold for 60 health
Request:
{
	“gold”: “integer” /* how much gold invested into health */
}
Response:
{
	“health”: “integer” /* return updated health (old + updated from gold) */
}

Technical Flows

Example 1:

Loli Boppi Gameplay:

We will make a pro boxer named Loli Boppi. We start off by calling POST /create-user/Loli-Boppi, and we get back her user id. Loli Boppi comes into our shop, asking to buy an animal for a fight. She starts off by getting a catalog of the animals by calling a GET /catalog. Loli Boppi comes in with 200 gold, and let’s say she was interested in an animal named Feefee that cost 70 gold. She then calls POST /buy-animal/Feefee. She is then charged 70 gold and is left with 130 gold and Feefee afterwards.

Example 2: 

Ash Ketchum’s Gameplay:

Ash starts by creating his account using:
	POST ‘/create-user/Ash-Ketchum’
This sets his profile up with 200 gold and 100 health. 

He then looks through the catalog with GET ‘/catalog/’  to view all the available animals, and chooses a monkey for 65 gold. 
He calls POST ‘/buy-animal/Monkey’, and he is left with 135 gold. 

He wants to fight, and uses POST ‘/fight/’ with
{
    "user_id": Ash’s user ID,
    "animal-use": true,
    "payment": 10
}
He now has 125 gold. 

Afterwards, he uses GET ‘/fight-result/’ to find out he won the fight, earning him 110 gold (100 gold bonus plus 10 gold victory reward). He now has 235 gold.


Example 3:

Steve Irwin’s Gameplay:

Steve starts by creating his account using:
	POST ‘/create-user/Steve-Irwin’
This sets his profile up with 200 gold and 100 health. 

He then looks through the catalog with GET ‘/catalog/’  to view all the available animals, and chooses an alligator for 140 gold. 
He calls POST ‘/buy-animal/, and he is left with 60 gold. 

He wants to fight, and uses POST ‘/fight/’ with
{
    "user_id": Irwin,
    "animal-use": true,
    "payment": 50
}

He loses, and now has 10 gold. 

To recover, Steve uses POST ‘/restock/’ to spend 5 gold for 10 health points, and he's got just 5 gold left. 
He wants to know his standings, so uses GET ‘/leaderboard/’ to see he is in last place.
