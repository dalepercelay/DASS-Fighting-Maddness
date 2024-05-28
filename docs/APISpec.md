<h1>API Specification for Group Project:</h1>

**List of API calls:**

1. `Get Catalog of Animals` (all animals available to be bought)
2. `Create an Animal` (user can create an animal to catalog and get money that way)
3. `Create User` (id, name, gold, animal, health status for user)
4. `Buy an Animal` (for one fight at a time)
5. `Create a Fight` (pay up to 10 gold to fight, gets 0 - 100 chance of winning – higher if higher stats)
6. `Leaderboard` (after every fight result updates, the leaderboard updates)
7. `Restock on Resources` (buying health)

**Get Catalog of Animals - GET Method** `/catalog`
Description: Gets a catalog of all the animals available for purchase. One user can have multiple animals at a time - when they get the animal, it is removed from catalog by their availability = FALSE.

Response:

```
[
	{
		“id”: “integer”
		“name”: “string”
		“attack”: “integer” /* between 1 and 80 */
		"defense": "integer" /* between 1 and 80 */
		“price”: “integer”
	}
]
```

**Create an Animal - POST Method `/animal/create`**
Description: Users can create animals (with given name, stats - we create id). Price is equal
to attack + defense. All animals have distinct names and ids.
Request:

```
{
	“aniaml_name”: “string”
	"attack": "integer" /* between 1 and 80 */
	“defense”: “integer” /* between 1 and 80 */
}
```

Response:

```
{
	"created animal id {animal_id}: {animal_name}, {attack}, {defense}"
}
```

**Create User - POST Method `/user/create`**
Description: Given a name, it creates a user which has a starting gold of 200, and no animals for fighting. All users must have unique names.
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

**Buy an Animal - PUT Method `/animal/buy`**
Description: Buy an animal (if the user has enough gold). Return True if delivery was successful (user had enough gold to buy) otherwise False. (An animal starts with 100 health. If their health gets <=10, a user can restore the animal's health, otherwise the animal will be unable to fight)
Request:

```
{
	“animal_id”: "integer"
	"user_id": "integer"
}
```

Response:

```
{
	“delivery-status”: “boolean”
}
```

**Create a Fight - POST Method `/fight`**
Description: Users can initiate fights with preset enemies to earn gold. Users will pay any amount of gold (basically betting in your luck) in order to participate in the fight. A random enemy will be picked out in the database table called Enemies to fight, and they will have their own respective stats, health, and name.

There will be three rounds of fighting total. Each round, for both sides, there will be a probability from 1 - 35 and whatever that number is, it will be subtracted from the main health points. Whoever has the lowest amount of health by the end of the three rounds will be the winner, and of course if one side has less than 0 or reached 0 health points, then automatically the other side wins. The 1 - 35 is just an average range of health points you can lose in one round. The higher the defense and attack stats are, the lower the range can go to decrease the amount of health points you lose. Vice versa for the lower the defense and attack stats are, the higher the range of points you can lose will be.

Winning the fight would allow them to earn money based on how much they choose to bet their gold by 10. For example, if a user bet 10 gold and won the battle, then they can get 100 gold total from the battle (aka bonus) plus 10 gold as a base congratulations reward. If they lose the fight though, they just lose the gold they originally bet in the first place. Furthermore, if they lose, their animal' health is decreased by 20.

Additionally, if their animal is too weak (health is less than or equal to 10) because the user hasn't restocked them, they will be unable to fight!!

Request:

```
{
	“user_id”: “integer”
	"animal_id": integer"
	“payment”: “integer”
}
```

Response:

```
{
	"animal used to fight": "string"
	"reward": "integer"
	"bonus": "integer"
	"enemy fought": "string"
	"winner": "string"
}
```

**Leaderboard - GET Method `/leaderboard`**
Description: Everyday, the leaderboard would be updated based on the rankings of users with the highest amount of gold

Response: (ordered by number of gold in ascending order)

```
{
	“name”: “string” /* user name */
	“gold”: “string” /* how much gold the user has */
}
```

**Restock on Resources - POST Method `/inventory/restore`**
Description: After every fight/battle, the user will need to purchase gold to restock their animal's health accordingly. They will purchase 10 gold for 20 health, 20 gold for 40 health, and 30 gold for 60 health.

The maximum health they can fill up to is back to 100.

Request:

```
{
	"user_id": "integer",
	"animal_id": "integer,
	“gold”: “integer” /* how much gold invested into health */
}
```

Response:

```
{
	"restored {health} health with {gold} gold"
}
```

**Get Inventory - GET Method `/inventory`**
Description: Retrieve user inventory
Request:

```
{
	"user_id": “int”
}
```

Response:

```
{
	"gold": "integer"
	"animals":
		[
			"animal_id": "integer"
			"animal_name": "string"
			"health": "integer"
		]
}
```
