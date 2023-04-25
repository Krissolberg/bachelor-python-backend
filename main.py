from typing import List
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.apiExtentions.shodanSok import shoSearch
from backend.apiExtentions.shodanGetService import verifyShodanKey, shodanDNS
from backend.databaseFunc import verifyConnection, getDatabases, getCol, getDataCol, findDocu, deleteOne, insertOne, \
    insertMany
from backend.auth import createNewUser, userLogin, updateUserPassword, getUserinfo, validToken, updateSavedSearch, \
    removeSavedSearch

description = """
## Hvis noe ikke fungerer
### *Sjekk første funksjon i shodan og mongodb. Hvis en av disse ikke fungerer, så vil ingenting fungere!*
"""

tags_metadata = [
    {
        "name": "profile",
        "description": "Login/Register/Forgot"
    },
    {
        "name": "shodan",
        "description": "Operations with Shodan-API",
        "externalDocs": {
            "description": "Link to offical Shodan REST API Doc",
            "url": "https://developer.shodan.io/api"
        },
    },
    {
        "name": "mongodb",
        "description": "Operations with the database",
        "externalDocs": {
            "description": "Link to offical PyMongo Doc",
            "url": "https://pymongo.readthedocs.io/en/stable/"
        },
    }
]

app = FastAPI(
    title='Bachelor Backend',
    description=description,
    version='0.0.1',
    openapi_tags=tags_metadata)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def root():
    return "Good day, sir!"


@app.get("/shodankeyverifier", tags=["shodan"])
def verify_shodan_key():
    try:
        return verifyShodanKey()
    except:
        raise HTTPException(status_code=401, detail="Invalid ShodanAPI-key. Could not connect to Shodan.")


# ... er det samme som Required fra pydantic


@app.get("/login", tags=["profile"])
async def login(email: str, password: str, remember: bool):
    return userLogin(email, password, remember)


@app.post("/register", tags=["profile"])
async def register(user: str, role: bool, email: str, password: str):
    return createNewUser(user, role, email, password)


@app.get("/userinfo", tags=["profile"])
async def userinfo(token):
    return getUserinfo(token)


@app.put("/updatePassword", tags=["profile"])
async def updatePassword(email: str, password: str, new_password: str):
    return updateUserPassword(email, password, new_password)


@app.get("/checkToken", tags=["profile"])
async def checkToken(token: str):
    return validToken(token)


@app.get("/getLoggedSearch", tags=["profile"])
async def getLoggedSearch(token: str):
    try:
        return getUserinfo(token)['logSearch']
    except:
        raise HTTPException(status_code=401, detail="Invalid credentials. Token is not valid")


@app.get("/getSavedSearch", tags=["profile"])
async def getSavedSearch(token: str):
    try:
        return getUserinfo(token)['savedSearch']
    except:
        raise HTTPException(status_code=401, detail="Invalid credentials. Token is not valid")


@app.delete("/removeOneSavedSearch", tags=["profile"])
async def removeSearch(token: str, removeArray: List[str] = Query(...)):
    try:
        return removeSavedSearch(token, removeArray)
    except:
        raise HTTPException(status_code=401, detail="Invalid credentials. Token is not valid")


# ------------------------------------------------------------------------#

@app.get("/search", tags=["shodan"])
async def shodan_search(auth: str, url_ip: List[str] = Query(...)):
    check = updateSavedSearch(auth, url_ip)
    if check:
        return shoSearch(url_ip)
    else:
        raise HTTPException(status_code=401, detail="Invalid ShodanAPI-key or Auth-token. Could not connect to Shodan.")


@app.get("/single", tags=["shodan"])
async def single_search(auth: str, url_ip: str = Query(...)):
    check = updateSavedSearch(auth, [url_ip])
    if check:
        return shoSearch([url_ip])
    else:
        raise HTTPException(status_code=401, detail="Invalid ShodanAPI-key or Auth-token. Could not connect to Shodan.")


@app.get("/orgsearch", tags=["shodan"])
async def org_search(auth: str, org: str = Query(...)):
    check = updateSavedSearch(auth, [f'org:{org}'])
    if check:
        return shoSearch([f'org:"{org}"'])
    else:
        raise HTTPException(status_code=401, detail="Invalid ShodanAPI-key or Auth-token. Could not connect to Shodan.")


@app.get("/dnssearch", tags=["shodan"])
async def dns_search(dns: str = Query(...)):
    try:
        return shodanDNS(dns)
    except:
        raise HTTPException(status_code=401, detail="Invalid ShodanAPI-key or Auth-token. Could not connect to Shodan.")


# ------------------------------------------------------------------------#

@app.get("/db/verifier", tags=["mongodb"])
async def verify_database_status():
    check = verifyConnection()
    if check:
        return check
    else:
        raise HTTPException(status_code=404, detail="Could not reach MongoDB. MongoDB is not in active state.")


@app.get("/db/getDBs", tags=["mongodb"])
async def get_db():
    check = getDatabases()
    if check:
        return check
    else:
        raise HTTPException(status_code=404, detail="Could not reach MongoDB. MongoDB is not in active state.")


@app.get("/db/getCol", tags=["mongodb"])
async def get_col(db: str = Query(...)):
    check = getCol(db)
    if check:
        return check
    else:
        raise HTTPException(status_code=404, detail="Could not find given database. Is MongoDB running?")


@app.get("/db/getData", tags=["mongodb"])
async def get_data(db: str = Query(...), col: str = Query(...)):
    check = getDataCol(db, col)
    if check:
        return check
    else:
        raise HTTPException(status_code=404, detail="Could not find given database and collection. Is MongoDB running?")


@app.get("/db/findDocu", tags=["mongodb"])
async def find_docu(db: str = Query(...), name: str = Query(...)):
    check = findDocu(db, name)
    if check:
        return check
    else:
        raise HTTPException(status_code=404, detail="No result.")


@app.post("/db/insertOne", tags=["mongodb"])
async def insertOne(db: str = Query(...), col: str = Query(...), name: str = Query(...), description: str = Query(...)):
    return insertOne(db, col, name, description)


@app.post("/db/insertMany", tags=["mongodb"])
async def insertMany(db: str = Query(...), col: str = Query(...), name: List[str] = Query(...),
                     description: List[str] = Query(...)):
    return insertMany(db, col, name, description)


@app.put("/db/updateOne", tags=["mongodb"])
async def updateOne(db: str = Query(...), col: str = Query(...), name: str = Query(...), description: str = Query(...)):
    return updateOne(db, col, name, description)


@app.delete("/db/deleteOne", tags=["mongodb"])
async def deleteOne(db: str = Query(...), col: str = Query(...), name: str = Query(...)):
    return deleteOne(db, col, name)
