# Mysql INNODB Docker-Compose

## Selecting:

### Query:

Query Type = 1


```SELECT * FROM Users WHERE Users.date_of_birth='1936-07-24' LIMIT 500;```

Query Type = 2

```SELECT * FROM Users WHERE Users.date_of_birth>='1936-07-24' LIMIT 500;```

Query Type = 3

```SELECT * FROM Users WHERE Users.date_of_birth>='1936-07-24' ORDER BY Users.date_of_birth LIMIT 500;```


### Results:

| Index Type       | Query Type = 1 | Query Type = 2 | Query Type = 3 |
|------------------|:--------------:|----------------|----------------|
| Without Index    |   3 s 103 ms   | 24 ms          | 11 s 933 ms    |
| With Btree Index |     47 ms      | 47 ms          | 31 ms          |
| With HASH Index  |     28 ms      | 48 ms          | 36 ms          |


## Inserting:


### Query:

Insert 50000 rows by `put_data.py` file

### Results


| Type             | trx_commit = 1 | trx_commit = 2 | trx_commit = 0 |
|------------------|:--------------:|----------------|----------------|
| Without Index    |     6.81 s     | 6.68 s         | 6.55 s         |
| With BTree Index |    36.41 s     | 9.05 s         | 7.17 s         |
