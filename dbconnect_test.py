import dotenv
import os
import datetime

import pymongo

dotenv.load_dotenv()
DBUSER = os.getenv('DBUSER')
DBPASS = os.getenv('DBPASS')
DBURI = os.getenv('DBURI')
CONNECT_STR = f"mongodb+srv://{DBUSER}:{DBPASS}@{DBURI}/?retryWrites=true&w=majority"

client = pymongo.MongoClient(CONNECT_STR)
db = client

packs = client.db.packs

package = {
    "id" : "123",
    "shelf_id" : "987",
    "timestamp" : datetime.datetime.now()
}

packs.insert_one(package)

print(packs)