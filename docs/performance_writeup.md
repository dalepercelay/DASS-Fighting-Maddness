V5

# Fake Data Modeling
Python file to insert 1M rows: https://github.com/dalepercelay/DASS-Fighting-Maddness/blob/main/src/localdatabase.py
In this file, we create 100,000 users, 400,000 animals, and 20,000 enemies. Since we create 100,000 users and 400,000 animals, we also insert 500,000 rows into transactions to model the starting gold and health. We believe our service should scale in this way because each user can have multiple animals and we thought 4 animals / user was a good average evening out for those who may only have 1 vs those who may buy many many animals. 20,000 just seemed like a good number for enemies to add variety since in our endpoints we never add/kill enemies (just a preset pool of potential enemies). The other tables such as fights and animals_owned depend on the endpoints such as buying animals or creating a fight so we did not insert fake model data. In total, we create 1,020,000 rows of data.

# Performance results of hitting endpoints
Slowest endpoints (slowest to fastest): get inventory, create animal, leaderboard
Endpoint timings:
Get inventory: 438.818ms
Restore Health: 149.838ms
Catalog: 101.665ms
Create user: 104.404ms
Create animal: 209.707ms
Buy animal: 75.843ms
Leaderboard: 166.538ms
Fight: 79.788ms

# Performance tuning
 Get inventory
Explain results:
Create index SQL:
Explain results (after creating index):
Performance improved?:

Create animal
Explain results:
Create index SQL:
Explain results (after creating index):
Performance improved?:

Leaderboard
Explain results:
Create index SQL:
Explain results (after creating index):
Performance improved?: