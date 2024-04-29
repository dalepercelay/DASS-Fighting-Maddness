<h1>API Specification for Group Project:</h1>

<h2>**List of API calls:**</h2>
1. `Get Catalog of Animals` (all animals available to be bought)
2. `Create an Animal` (user can create an animal to catalog and get money that way)
3. `Create User` (id, name, gold, animal, health status for user)
4. `Buy an Animal` (for one fight at a time)
5. `Create a Fight` (pay 10 gold to fight, gets 0 - 100 chance of winning – higher if higher stats)
6. `Fight Result Update` (get money if win, lose health)
7. `Leaderboard` (after every fight result updates, the leaderboard updates)
8. `Restock on Resources` (buying health)

<h2>**Get Catalog of Animals - GET Method `/catalog/`**</h2>
Description: Gets a catalog of all the animals available for purchase. Only one user can have an animal at a time - when they get the animal, it is removed from catalog.
Response:
```
{ 
	“id”: “integer”
	“name”: “string”
	“stats”: “integer” /* between 1 and 100 */
	“price”: “integer” 
}
```

<h2>**Create an Animal - POST Method `/create-animal/{name}`**</h2>
Description: Users can create animals (with given name, stats, price - we create id) and it can be considered an investment. It will take 100 gold for users to create an animal, but once they sell it to the main store, they can sell it for 50 no matter what animal it is. But then the users can create a price to sell their animals for in the catalog. 
Request:
```{
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
<h2>**Create User - POST Method `/create-user/{name}`**</h2>
Description: Given a name, create a user which has starting gold 200, no animal, 100 health status (from 0 - 100) for the user.
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
<h2>**Buy an Animal - POST Method `/buy-animal/{name}`**</h2>
Description: Given an animal id from the catalog, buy an animal (if the user has enough gold). Return if delivery was successful (user had enough gold to buy).
(An animal starts with 100 health. If their health gets to 0, they cannot be used by the user anymore)
Request:
```
{
	“name”: “string”
}
```
Response:
```
{
	“delivery-status”: “boolean”
}
```
<h2>**Create a Fight - POST Method `/fight/`**</h2>
Description: Everyday, there will be one main fight/battle. Users will pay 0 - 10 gold in order to participate in the fight. A random enemy will be picked out in the database table called Enemies to fight, and they will have their own respective stats, health, and name.

There will be three rounds of fighting total. Each round, for both sides, there will be a probability from 1 - 35 and whatever that number is, it will be subtracted from the main health points. Whoever has the lowest amount of health by the end of the three rounds will be the winner, and of course if one side has less than 0 or reached 0 health points, then automatically the other side wins. The 1 - 35 is just an average range of health points you can lose in one round. The higher the defense and attack stats are, the lower the range can go to decrease the amount of health points you lose. Vice versa for the lower the defense and attack stats are, the higher the range of points you can lose will be.

Request:
```
{
	“user_id”: “integer”
	“animal-use”: “boolean” /* true if using their animal */
	“payment”: “integer” /* between 1 - 10 */
}
```
Response:
```
{
	“success”: “boolean”
}
```
<h2>**Fight Result Update - GET Method `/fight-result/`**</h2>
Description: Winning the fight would allow them to earn money based on how much they choose to bet their gold by 10. For example, if a user bet 10 gold and won the battle, then they can get 100 gold total from the battle (aka bonus) plus 10 gold as a congratulations reward. If they lose the fight though, they just lose the gold they originally bet in the first place. Furthermore, if they lose, their animal' health is decreased by 20. 
Response:
```
{
	“reward”: “integer” 10 (if they win) or 0 (if they lose),
	“bonus”: “integer” (amount of gold user bet) * 10 (if they win) or 0 (if they lose)
}
```
<h2>**Leaderboard - GET Method `/leaderboard/`**</h2>
Description: Everyday, the leaderboard would be updated based on the rankings of users with the highest amount of gold
Response: (ordered by number of gold)
```
{
	“name”: “string” /* user name */
	“gold”: “string” /* how much gold the user has */
}
```
<h2>**Restock on Resources - POST Method `/restock/`**</h2>
Description: After every fight/battle, the user will need to purchase gold to restock their health accordingly. They will purchase 10 gold for 20 health, 20 gold for 40 health, and 30 gold for 60 health
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
