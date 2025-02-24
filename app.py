from fastapi import FastAPI, HTTPException, Response
from fastapi.encoders import jsonable_encoder
import motor.motor_asyncio
from pydantic import BaseModel, BeforeValidator, Field
from fastapi.responses import JSONResponse
from typing import Annotated, List
from bson import ObjectId
from datetime import datetime
from dotenv import load_dotenv
import os 
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
app = FastAPI()

origins = [ "https://ecse3038-lab3-tester.netlify.app" ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

connection = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGODB_URL"))
profile_db = connection.profile
collection = profile_db["profiles"]

PyObbjectId = Annotated[str, BeforeValidator(str)]

class Profile(BaseModel):
    id: PyObbjectId | None = Field(default = None, alias="_id")
    last_updated: datetime = datetime.now()
    username: str
    color: str
    role: str

class ProfileCollection(BaseModel):
    profile: List[Profile]

# class ProfileUpdate(BaseModel):
#     last_updated: datetime = datetime.now()
#     username: str | None = None
#     color: str | None = None
#     role: str | None = None


class Tank(BaseModel):
    id: PyObbjectId | None = Field(default = None, alias="_id")
    location: str
    lat: str
    long: str

class TankCollection(BaseModel):
    tanks: List[Tank]

class Tank_Update(BaseModel):
    location: str | None = None
    lat: str | None = None
    long: str | None = None

@app.get("/profile")
async def get_profiles():
    profile_collection = await profile_db["profiles"].find().to_list(999)
    return ProfileCollection(profile=profile_collection)

@app.post("/profile")
async def create_profile(profile_request: Profile):
    profile_dictionary = profile_request.model_dump()
    created_profile = await profile_db["profiles"].insert_one(profile_dictionary)

    profile = await profile_db["profiles"].find_one({"_id":created_profile.inserted_id})
    temp = Profile(**profile)
    profile_json = jsonable_encoder(temp)
    return JSONResponse(profile_json, status_code=201)

@app.patch("/tank/{tank_id}")
async def update_tank(tank_id: str, tank_update: Tank_Update):
    updated_tank = await profile_db["tank"].find_one({"_id":ObjectId(tank_id)})
    if updated_tank:
        tank_dictionary = tank_update.model_dump(exclude_unset=True)
        updated_tank = await profile_db["tank"].update_one({"_id":ObjectId(tank_id)},{"$set":tank_dictionary})
        updated_tank = await profile_db["tank"].find_one({"_id":ObjectId(tank_id)})
        # Profile.last_updated = datetime.now()
        profile_db["profiles"].update_many(
            {"active": True},  # Filter for active profiles
            {"$set": {"last_updated": datetime.now()}}  )

        return Tank(**updated_tank)
    raise HTTPException(status_code=404,detail="Tank not found")

@app.get("/tank")
async def get_tanks():
    tank_collection = await profile_db["tank"].find().to_list(999)
    return TankCollection(tanks=tank_collection)
    
@app.post("/tank")
async def create_tank(tank_request: Tank):
    tank_dictionary = tank_request.model_dump()
    created_tank = await profile_db["tank"].insert_one(tank_dictionary)

    tank = await profile_db["tank"].find_one({"_id":created_tank.inserted_id})
    # Profile.last_updated = datetime.now()
    profile_db["profiles"].update_many(
            {"active": True},  # Filter for active profiles
            {"$set": {"last_updated": datetime.now()}}  )
    temp = Tank(**tank)
    tank_json = jsonable_encoder(temp)
    return JSONResponse(tank_json, status_code=201)

@app.delete("/tank/{tank_id}")
async def remove_tank(tank_id:str):  
    search_tank = await profile_db["tank"].find_one({"_id":ObjectId(tank_id)})
    if search_tank:
       await profile_db["tank"].delete_one({"_id":ObjectId(tank_id)})
    #    Profile.last_updated = datetime.now()
       profile_db["profiles"].update_many(
            {"active": True},  # Filter for active profiles
            {"$set": {"last_updated": datetime.now()}}  )
       return Response(status_code=200)
    
    raise HTTPException(status_code=404,detail="tank not found")

