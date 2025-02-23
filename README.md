<Lab_4>

<async def get_profiles():>
    <Displays all profiles created and stored in a collection>

<async def create_profile(profile_request: Profile):>
    <Takes profile information from client and create a new profile in MongoDB. If the profile is successfully created, an id is assigned to that profile and the client receives a summary of the created profile with a HTTP code 201.>

<async def update_tank(tank_id: str, tank_update: Tank_Update):>
    <Takes 3 field updates in from the client and update a record with the matching id. If no matching record is found, the client receives a 404 error code with details: tank not found>

<async def get_tanks():>
    <Displays all tanks created and stored in a collection>

<async def create_tank(tank_request: Tank):>
    <Takes tank information from client and create a new tank item in MongoDB database. If the profile is successfully created, an id is assigned to that profile and the client receives a summary of the created profile with a HTTP code 201.>

<async def remove_tank(tank_id:str):>
    <Searches the database for a record or item with the matching id. If a match is found, the record of tank is removed, else if no matches is found, the client receives a 404 error code with details: tank not found>

**Reason the code was written**
    <To explore using an actual database to store information on a profile and tanks in two collections>

<*Your favourite low effort/non-fancy food*>
    <As odd as it sounds, I do not have one. Matter of fact, I actually do not have a favourite of most things>