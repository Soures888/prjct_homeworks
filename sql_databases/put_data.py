import time

from faker import Faker
import mysql.connector

fake = Faker()

db = mysql.connector.connect(
  host="localhost",
  user="test",
  password="test",
  database="test",
  autocommit=False
)

cursor = db.cursor()
batch_size = 1000
insert_query = "INSERT INTO Users (name, email, date_of_birth) VALUES (%s, %s, %s)"

print('Status: Starting to insert data.')
t = time.time()

for i in range(0, 50000, batch_size):
    data = [(fake.name(), fake.email(), fake.date_of_birth(minimum_age=18, maximum_age=90)) for _ in range(batch_size)]
    cursor.executemany(insert_query, data)
    print(f"Inserted {i} rows so far.")
    db.commit()

print(f"Status: Inserted 50000 rows in {time.time() - t} seconds.")

cursor.close()
db.close()