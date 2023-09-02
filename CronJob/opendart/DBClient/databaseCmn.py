import json
import pymongo
import DBClient.declaration as declaration

if declaration.MONGO_PORT == None or declaration.MONGO_PORT == "":
    conn = pymongo.MongoClient(host=f"mongodb://{declaration.MONGO_HOST}/{declaration.MONGO_NAME}")
else:
    conn = pymongo.MongoClient(host=declaration.MONGO_HOST,port=int(declaration.MONGO_PORT))

