import string
from datetime import datetime
import random
from fastapi import FastAPI
from elasticsearch import Elasticsearch
from pymongo import MongoClient


# Mongo connection setup
mongo_connection = MongoClient("mongodb://admin:secret@mongo:27017/")
mongo_db = mongo_connection["mongo_db"]
mongo_collection = mongo_db["test_collection"]

app = FastAPI(root_path="/fastapi")
es = Elasticsearch(['http://elasticsearch:9200'])
es_index_name = 'test_index'


@app.get("/esread")
async def root():
    # Specify the index you want to read from
    res = es.search(index=es_index_name, size=500,
                    body={"query": {"match_all": {}}})
    return res['hits']['hits']


@app.get("/mongoread")
async def mongo_read():
    # Query your MongoDB
    cursor = mongo_collection.find().limit(500)
    # Convert cursor to list of dicts
    data = [{**item, '_id': str(item['_id'])} for item in cursor]
    # Return the data
    return data


@app.get("/generate_data")
async def generate_data():

    # Clear the database
    mongo_collection.delete_many({})
    es.indices.delete(index=es_index_name, ignore=[400, 404])

    # Create Elasticsearch index
    es.indices.create(index=es_index_name, ignore=400)

    for _ in range(500):
        # Generate random data
        name = ''.join(random.choice(string.ascii_letters) for _ in range(5))
        address = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))

        mongo_collection.insert_one({"name": name, "address": address, "timestamp": datetime.now()})
        es.index(index=es_index_name, body={"name": name, "address": address, "timestamp": datetime.now()})

    return {"message": "Data has been generated and inserted."}

# Close connections at app shutdown

@app.on_event("shutdown")
async def shutdown_event():
    mongo_connection.close()
    es.close()

