import dotenv
import os
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

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

origins = [
    # TODO viisakamalt, see vajalik et brauser vastu võtaks neid pilte
    "http://localhost:3000",
    "http://localhost",
    "http://localhost:8080",
    "https://localhost:3000",
    "https://localhost",
    "https://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.post("/create")
async def create_package(req:Request):
    req = await req.json()
    packageIdList = req["packageIdList"]
    shelfId = req["shelfId"]
    print(packageIdList)
    print(shelfId)

    # put new thing to db
    for packId in packageIdList:
        package = {
            "id": packId,
            "shelf_id": shelfId,
            "timestamp": datetime.now(),
        }
        collection.insert_one(package)

    return {
        "message": "success",
        "debug": f"created packages {packageIdList}, on shelf {shelfId}",
    }


# takes in package, return the correct shelf_id
# also sends a request to the esp server
@app.get("/find")
async def find_package(package_id: str):
    # Important TODO: communicate to microcontroller the need to light up that shelf

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


@app.post("/test")
async def test(pack:Request):
    print(pack)
    req = await pack.json()
    print(req["pack_id"])
    return {"message": "success"}