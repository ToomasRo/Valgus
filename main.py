import dotenv
import os
from datetime import datetime

from fastapi import FastAPI
import pymongo

# db connection
dotenv.load_dotenv()
DBUSER = os.getenv("DBUSER")
DBPASS = os.getenv("DBPASS")
DBURI = os.getenv("DBURI")
CONNECT_STR = f"mongodb+srv://{DBUSER}:{DBPASS}@{DBURI}/?retryWrites=true&w=majority"

client = pymongo.MongoClient(CONNECT_STR)
# db = client.test
collection = client.db.packs

app = FastAPI()


@app.post("/create")
async def create_package(package_id: str, shelf_id: str):
    # put new thing to db
    package = {
        "id": package_id,
        "shelf_id": shelf_id,
        "timestamp": datetime.now(),
    }

    collection.insert_one(package)

    return {
        "message": "success",
        "debug": f"created package_id {package_id}, on shelf {shelf_id}",
    }


# takes in package, return the correct shelf_id
# also sends a request to the esp server
@app.get("/find")
async def find_package(package_id: str):
    # query db
    query = {"id": package_id}
    all_documents = collection.find(query)
    shelf_ids = []
    for doc in all_documents:
        shelf_ids.append(doc["shelf_id"])
    print(shelf_ids)
    return {"message": shelf_ids, "debug": f"finding pakki {package_id}"}


@app.delete("/delete")
async def delete_package(package_id: str, mock: int = 1):
    # update db
    if mock == 1:
        print(f"Deleted package {package_id}")
    else:
        collection.delete_one({"id": package_id})

    return {"message": "success", "debug": f"deleted pack {package_id}"}


@app.get("/getall")
async def getall():
    all_documents = collection.find({})
    docs = []
    for doc in all_documents:
        docs.append(
            {
                "id": doc["id"],
                "shelf_id": doc["shelf_id"],
                "timestamp": doc["timestamp"],
            }
        )
    print(docs)
    return {"message": docs}
