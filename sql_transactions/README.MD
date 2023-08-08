# Sql Transactions Parallel Access Problems

## Lost Update Problem

A lost update problem occurs due to the update of the same record by two different transactions at the same time.

<table>
<tr>
<th> Transaction 1 </th>
<th> Transaction 2 </th>
</tr>
<tr>
<td>

```sql
BEGIN;
SELECT balance FROM users WHERE id = 1;
--- You will see a balance 100
```

</td>
<td>
</td>
</tr>
<tr>
<td></td>
<td>

```sql
BEGIN;
SELECT balance FROM users WHERE id = 1;
--- Here, you'll again see the balance is 100 since both transactions started almost simultaneously.
```

</td>
</tr>
<tr>
<td>

```sql
UPDATE users SET balance = balance - 20 WHERE id = 1;
--- Now, the balance in the tx is 80.
```
</td>
<td>
</td>
</tr>

<tr>
<td>
</td>
<td>



```sql
UPDATE users SET balance = balance + 30 WHERE id = 1;
COMMIT;
--- Now, the balance in the database is 130 instead of the expected 110 (100 - 20 + 30). If We Have Lost Update Problem.
```
</td>
</tr>
</table>

### PostgreSQL/MySQL(InnoDb) Lost Update test results

| Isolation Level |                                        PostgreSQL                                         | MySQL                                                                                                                                             |
|-----------------|:-----------------------------------------------------------------------------------------:|---------------------------------------------------------------------------------------------------------------------------------------------------|
| Serializable    | Avoided by *ERROR: could not serialize access due to concurrent update* at transaction #2 | Prevent by Locked, but need to add FOR UPDATE to avoid deadlocks. Because by default at the Serializable level MySQL automatically adds FOR SHARE |
| Repeatable read | Avoided by *ERROR: could not serialize access due to concurrent update* at transaction #2 | Prevent by LOCK at transaction #2 while update                                                                                                    |
| Read committed  |                      Avoided by LOCK at transaction #2 while update                       | Prevent by LOCK at transaction #2 while update                                                                                                    |
| Read uncommited |                                             -                                             | Prevent by LOCK at transaction #2 while update                                                                                                    |

## Dirty Read Problem

A dirty read (aka uncommitted dependency) occurs when a transaction retrieves a row that has been updated by another transaction that is not yet committed.


<table>
<tr>
<th> Transaction 1 </th>
<th> Transaction 2 </th>
</tr>
<tr>
<td>

```sql
BEGIN;
SELECT balance FROM users WHERE id = 1;
--- You will see a balance 100
```

</td>
<td>
</td>
</tr>
<tr>
<td></td>
<td>

```sql
BEGIN;
UPDATE users SET balance=150 WHERE id=1;
--- No commit here
```

</td>
</tr>
<tr>
<td>

```sql
SELECT balance FROM users WHERE id = 1;
--- If we have dirty read problem we will see a balance 150
```
</td>
<td>
</td>
</tr>
<tr>
<td>
</td>

<td>

```sql
ROLLBACK;
```
</td>
</tr>
</table>

### PostgreSQL/MySQL(InnoDb) Dirty Read test results

| Isolation Level | PostgreSQL | MySQL                                            |
|-----------------|:----------:|--------------------------------------------------|
| Serializable    |  Avoided   | Avoided by locking update for second transaction |
| Repeatable read |  Avoided   | Avoided                                          |
| Read committed  |  Avoided   | Avoided                                          |
| Read uncommited |     -      | <u>Reproduced</u>                                |

## Phantom reads Problem

A phantom read occurs when a transaction retrieves a set of rows twice and new rows are inserted into or removed from that set by another transaction that is committed in between.

<table>
<tr>
<th> Transaction 1 </th>
<th> Transaction 2 </th>
</tr>
<tr>
<td>

```sql
BEGIN;
SELECT email FROM users WHERE balance > 30;
--- You will get email of users: <bob>
```

</td>
<td>
</td>
</tr>
<tr>
<td></td>
<td>

```sql
BEGIN;
INSERT INTO users (name, email, balance) VALUES ('alice', 'alice@gmail.com', 40);
COMMIT;
```

</td>
</tr>
<tr>
<td>

```sql
SELECT email FROM users WHERE balance > 30;
--- If we have phantom reads problem we will get email of users: <bob, alice>
```
</td>
<td>
</td>
</tr>

</table>

### PostgreSQL/MySQL(InnoDb) Phantom Read test results

| Isolation Level | PostgreSQL | MySQL           |
|-----------------|:----------:|-----------------|
| Serializable    |  Avoided   | Avoided by Lock |
| Repeatable read |  Avoided   | Avoided         |
| Read committed  | Reproduced | Reproduced      |
| Read uncommited |     -      | Reproduced      |
