import dotenv
import os
from datetime import datetime

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import pymongo
import serial
# bluetooth microcontroller import
import utils.bluetoothConnection as btconn


# db connection
dotenv.load_dotenv()
DBUSER = os.getenv("DBUSER")
DBPASS = os.getenv("DBPASS")
DBURI = os.getenv("DBURI")
CONNECT_STR = f"mongodb+srv://{DBUSER}:{DBPASS}@{DBURI}/?retryWrites=true&w=majority"

client = pymongo.MongoClient(CONNECT_STR)
collection = client.db.packs

# setting up the bluetooth connection
try:
    btconn.init(os.getenv("COMPORT"))
except serial.serialutil.SerialException:
    print("Did not start bluetooth connection")

app = FastAPI()

origins = [
    # TODO viisakamalt, see vajalik et brauser vastu võtaks neid pilte
    "http://localhost:3000",
    "http://localhost",
    "http://localhost:8080",
    "https://localhost:3000",
    "https://localhost",
    "https://localhost:8080",
    "127.0.0.1:2137"
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex='.*',
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/create")
async def create_package(req: Request):

    try:
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

    except pymongo.errors.DuplicateKeyError as dke:
        print(dke)
        raise HTTPException(status_code=400, detail="Already existing package!")


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

    try:
        for shelf_id in shelf_ids:
            btconn.send(shelf_id)
    except Exception as e:
        print(e)


    return {"message": shelf_ids, "debug": f"finding pakki {package_id}"}


@app.delete("/delete")
async def delete_package(package_id: str, mock: int = 0):
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
async def test(pack: Request):
    print(pack)
    req = await pack.json()
    print(req["pack_id"])
    return {"message": "success"}
