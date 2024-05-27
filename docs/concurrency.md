 Dirty Reads in Animal Creation

Scenario: User A is in the process of creating a new animal, but the transaction has not been committed yet. Meanwhile, User B tries to fetch the list of animals, potentially seeing the uncommitted animal data from User A's transaction.

Phenomenon: Dirty Read
Isolation Level: Read Uncommitted
sequenceDiagram
    participant T1 as Transaction 1 (User A)
    participant T2 as Transaction 2 (User B)
    participant DB as Database

    T1->>DB: Insert new animal (uncommitted)
    T2->>DB: Select * from animals
    DB->>T2: Return uncommitted animal data
    T1->>DB: Commit
Non-Repeatable Reads in Buying an Animal

Scenario: User A reads their current gold balance in one transaction (T1). Before User A completes the transaction to buy an animal, User B adds or deducts some gold in a separate transaction (T2). When User A rechecks their gold balance in the same transaction (T1), the balance has changed.

Phenomenon: Non-Repeatable Read
Isolation Level: Read Committed
sequenceDiagram
    participant T1 as Transaction 1 (User A)
    participant T2 as Transaction 2 (User B)
    participant DB as Database

    T1->>DB: Read user's gold
    DB->>T1: Return gold amount
    T2->>DB: Update user's gold
    T2->>DB: Commit
    T1->>DB: Read user's gold again
    DB->>T1: Return updated gold amount



    Phantom Reads in Listing Owned Animals

Scenario: User A retrieves a list of animals they own in one transaction (T1). Meanwhile, User B buys a new animal and the transaction is committed. User A retrieves the list of owned animals again in the same transaction (T1) and sees the new animal that User B just bought.

Phenomenon: Phantom Read
Isolation Level: Repeatable Read
sequenceDiagram
    participant T1 as Transaction 1 (User A)
    participant T2 as Transaction 2 (User B)
    participant DB as Database

    T1->>DB: Read animals owned by User A
    DB->>T1: Return list of animals
    T2->>DB: User B buys new animal
    T2->>DB: Commit
    T1->>DB: Read animals owned by User A again
    DB->>T1: Return updated list of animals

for preventing issues
Locking Mechanisms: Use appropriate locking mechanisms (e.g., row locks, table locks) to control access to data during transactions.
Concurrency Control Strategies: Implement optimistic and pessimistic concurrency control strategies where appropriate.
MVCC: Use Multi-Version Concurrency Control (MVCC) to provide consistent snapshots of the data for read-heavy operations.