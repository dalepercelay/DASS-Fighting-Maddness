<h1>API Specification for Group Project:</h1>

**List of API calls:**
1. `Get Catalog of Animals` (all animals available to be bought)
2. `Create an Animal` (user can create an animal to catalog and get money that way)
3. `Create User` (id, name, gold, animal, health status for user)
4. `Buy an Animal` (for one fight at a time)
5. `Create a Fight` (pay up to 10 gold to fight, gets 0 - 100 chance of winning – higher if higher stats)
7. `Leaderboard` (after every fight result updates, the leaderboard updates)
8. `Restock on Resources` (buying health)

**Get Catalog of Animals - GET Method** `/catalog`
Description: Gets a catalog of all the animals available for purchase. One user can have an animal at a time - when they get the animal, it is removed from catalog by their availability = FALSE.
Response:
```
{ 
	“id”: “integer”
	“name”: “string”
	“attack”: “integer” /* between 1 and 100 */
	"defense": "integer" /* between 1 and 100 */
	“price”: “integer”
}
```

**Create an Animal - POST Method `/create-animal/{name}`**
Description: Users can create animals (with given name, stats, price - we create id) and it can be considered an investment. It will take 100 gold for users to create an animal, but once they sell it to the main store, they can sell it for 50 no matter what animal it is. But then the users can create a price to sell their animals for in the catalog. 
Request:
```
{
	“name”: “string”
	“defense”: “integer” /* between 1 and 50 */
	"attack": "integer" /* between 1 and 50 */
	“price”: “integer”
}
```
Response:
```
{
	“success”: “boolean”
}
```
**Create User - POST Method `/create-user/{name}`**
Description: Given a name, it creates a user which has a starting gold of 200, and no animals for fighting.
Request:
```
{
	“name”: “string”
}
```
Response:
```
{
	“user_id”: “integer”
}
```
**Buy an Animal - POST Method `/buy-animal/{animal_name}`**
Description: Buy an animal (if the user has enough gold). Return True if delivery was successful (user had enough gold to buy) otherwise False. (An animal starts with 100 health. If their health gets to 0, they cannot be used by the user anymore)
Request:
```
{
	“animal_name”: “string”
	"user_name": "string"
}
```
Response:
```
{
	“delivery-status”: “boolean”
}
```
**Create a Fight - POST Method `/fight/`**
Description: Everyday, there will be one main fight/battle. Users will pay any amount of gold (basically betting in your luck) in order to participate in the fight. A random enemy will be picked out in the database table called Enemies to fight, and they will have their own respective stats, health, and name.

There will be three rounds of fighting total. Each round, for both sides, there will be a probability from 1 - 35 and whatever that number is, it will be subtracted from the main health points. Whoever has the lowest amount of health by the end of the three rounds will be the winner, and of course if one side has less than 0 or reached 0 health points, then automatically the other side wins. The 1 - 35 is just an average range of health points you can lose in one round. The higher the defense and attack stats are, the lower the range can go to decrease the amount of health points you lose. Vice versa for the lower the defense and attack stats are, the higher the range of points you can lose will be.

Winning the fight would allow them to earn money based on how much they choose to bet their gold by 10. For example, if a user bet 10 gold and won the battle, then they can get 100 gold total from the battle (aka bonus) plus 10 gold as a congratulations reward. If they lose the fight though, they just lose the gold they originally bet in the first place. Furthermore, if they lose, their animal' health is decreased by 20.

Additionally, if their animal is too weak (health is less than or equal to 10) because the user hasn't restocked them, they will lose that animal completely so it's important to occassionally check up on the inventory!!

Request:
```
{
	“user_id”: “integer”
	“payment”: “integer”
}
```
Response:
```
{
	"reward": "integer"
	"bonus": "integer"
	"enemy fought": "string"
	"winner": "string"
}
```

**Leaderboard - GET Method `/leaderboard/`**
Description: Everyday, the leaderboard would be updated based on the rankings of users with the highest amount of gold

Response: (ordered by number of gold in ascending order)
```
{
	“name”: “string” /* user name */
	“gold”: “string” /* how much gold the user has */
}
```
**Restock on Resources - POST Method `/restock/`**
Description: After every fight/battle, the user will need to purchase gold to restock their animal's health accordingly. They will purchase 10 gold for 20 health, 20 gold for 40 health, and 30 gold for 60 health.

The maximum health they can fill up to is back to 100.

Request:
```
{
	“gold”: “integer” /* how much gold invested into health */
}
```
Response:
```
{
	“health”: “integer” /* return updated health (old + updated from gold) */
}
```

**Get Inventory - GET Method `/inventory/audit`**
Description: Retrieve user inventory
Request:
```
{
	“username”: “str”
}
```
Response:
```
{
	"gold": "integer"
	“animal”: “str” (name of animal if it has one, otherwise it will return -1)
	"health": "integer"
}
