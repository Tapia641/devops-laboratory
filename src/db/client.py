# from pymongo.mongo_client import MongoClient
# from pymongo.server_api import ServerApi

# CONNECTS WITH MONGODB
from pymongo import MongoClient

uri = "mongodb+srv://root:mDuBz9JFoc739CLD@cluster0.w2ugb5k.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
# db_client = MongoClient(uri)



# mongodb://127.0.0.1:27017
# db_client = MongoClient(host="mongodb://127.0.0.1", port=27017).local.employees
# db_client = MongoClient(host="127.0.0.1", port=27017)
db_client = MongoClient(host=uri, port=27017)


"""
docker pull mongodb/mongodb-community-server

docker run --name mongo -d -p 27017:27017 mongodb/mongodb-community-server:latest

docker exec -it mongo mongosh

# Connect to MongoDB with authentication
db_client = MongoClient("mongodb://username:password@localhost:27017/")

db.adminCommand('listDatabases');

use local

db.employees.find()
"""
