import string
from datetime import datetime
import random
from fastapi import FastAPI
from elasticsearch import Elasticsearch
import mysql.connector


# MySQL connection setup
mydb = mysql.connector.connect(
  host="mysql",
  user="dbuser",
  password="dbpassword",
  database="dbname"
)

app = FastAPI(root_path="/fastapi")
es = Elasticsearch(['http://elasticsearch:9200'])
es_index_name = 'test_index'


@app.on_event("startup")
async def startup_event():
    # Create Elasticsearch index
    es.indices.create(index=es_index_name, ignore=400)

    # Create MySQL table
    mycursor = mydb.cursor()
    mycursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        address VARCHAR(255)
    )
    """) # Adjust this query according to your table schema


@app.get("/esread")
async def root():
    # Specify the index you want to read from
    res = es.search(index=es_index_name, size=500,
                    body={"query": {"match_all": {}}})
    return res['hits']['hits']


@app.get("/mysqlread")
async def mysql_read():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM orders LIMIT 500")  # Change with your query
    myresult = mycursor.fetchall()
    return myresult


@app.get("/generate_data")
async def generate_data():
    mycursor = mydb.cursor()
    sql = "INSERT INTO orders (name, address) VALUES (%s, %s)"
    for _ in range(500):
        # Generate random data
        name = ''.join(random.choice(string.ascii_letters) for _ in range(5))
        address = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
        mycursor.execute(sql, (name, address))
        es.index(index=es_index_name, body={"name": name, "address": address, "timestamp": datetime.now()})
    mydb.commit()
    return {"message": "Data has been generated and inserted."}

