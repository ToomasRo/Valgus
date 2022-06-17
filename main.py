import dotenv
import os

from fastapi import FastAPI
import pymongo

# db connection
dotenv.load_dotenv()
DBUSER = os.getenv("DBUSER")
DBPASS = os.getenv("DBPASS")
DBURI = os.getenv("DBURI")
CONNECT_STR = f"mongodb+srv://{DBUSER}:{DBPASS}@{DBURI}/?retryWrites=true&w=majority"

client = pymongo.MongoClient(CONNECT_STR)
db = client.test

app = FastAPI()


@app.post("/create")
async def create_package(package_id: str, shelf_id: str):
    # put new thing to db
    return {"message": f"created package_id {package_id}, on shelf {shelf_id}"}


# takes in package, return the correct shelf_id
# also sends a request to the esp server
@app.get("/find")
async def find_package(package_id: str):
    # query db
    return {"message": f"finding pakki {package_id}"}


@app.delete("/delete")
async def delete_package(package_id: str):
    # update db
    return {"message": f"kustutasime pakki {package_id}"}
