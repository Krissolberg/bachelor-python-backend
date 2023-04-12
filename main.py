from typing import List
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from backend.shodanFunc import keyVerifier, sok, dnsSok
from backend.databaseFunc import verifyConnection, getDatabases, getCol, getDataCol, findDocu, deleteOne, insertOne, insertMany

description = """
Backend for Bachelorprosjektet.

## Shodan
Ikke glem å sette inn API-nøkkel før du fortsetter!!

Prøv med *keyverifier* om API-nøkkelen fungerer!

NB: Sjekk at MongoDB kjører, hvis den ikke gjør vil ingen API kall untatt *keyverifier* fungere!

## MongoDB
Her har vi ulike DB funksjoner
"""

tags_metadata = [
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
    },
    {
        "name": "profile",
        "description": "Login/Register/Forgot"
    },
    {
        "name": "profileData",
        "description": "Saved IPs/Url"
    },
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
    return keyVerifier()


@app.get("/search", tags=["shodan"])
async def shodan_search(url_ip: List[str] = Query(...)):
    return sok(url_ip)


# ... er det samme som Required fra pydantic

@app.get("/single", tags=["shodan"])
async def single_search(url_ip: str = Query(...)):
    return sok([url_ip])


@app.get("/orgsearch", tags=["shodan"])
async def org_search(org: str = Query(...)):
    return sok([f'org:"{org}"'])


@app.get("/dnssearch", tags=["shodan"])
async def dns_search(dns: str = Query(...)):
    return dnsSok(dns)


# ------------------------------------------------------------------------#

@app.get("/db/verifier", tags=["mongodb"])
async def verify_database_status():
    return verifyConnection()


@app.get("/db/getDBs", tags=["mongodb"])
async def get_db():
    return getDatabases()


@app.get("/db/getCol", tags=["mongodb"])
async def get_col(db: str = Query(...)):
    return getCol(db)


@app.get("/db/getData", tags=["mongodb"])
async def get_data(db: str = Query(...), col: str = Query(...)):
    return getDataCol(db, col)


@app.get("/db/findDocu", tags=["mongodb"])
async def find_docu(db: str = Query(...), navn: str = Query(...)):
    return findDocu(db, navn)


@app.post("/db/insertOne", tags=["mongodb"])
async def insertOne(db: str = Query(...), col: str = Query(...), navn: str = Query(...), beskrivelse: str = Query(...)):
    return insertOne(db, col, navn, beskrivelse)


@app.post("/db/insertMany", tags=["mongodb"])
async def insertMany(db: str = Query(...), col: str = Query(...), navn: List[str] = Query(...),
                     beskrivelse: List[str] = Query(...)):
    return insertMany(db, col, navn, beskrivelse)


@app.put("/db/updateOne", tags=["mongodb"])
async def updateOne(db: str = Query(...), col: str = Query(...), navn: str = Query(...), beskrivelse: str = Query(...)):
    return updateOne(db, col, navn, beskrivelse)


@app.delete("/db/deleteOne", tags=["mongodb"])
async def deleteOne(db: str = Query(...), col: str = Query(...), navn: str = Query(...)):
    return deleteOne(db, col, navn)


# ------------------------------------------------------------------------#
@app.get("login", tags=["profile"])
async def login(user: str, pw: str):
    return None


@app.post("register", tags=["profile"])
async def register(user: str, pw: str):
    return None


@app.get("geturl", tags=["profileData"])
async def geturl(user: str):
    return None


@app.post("addurl", tags=["profileData"])
async def addurl(user: str, data: str):
    return None


@app.delete("removeurl", tags=["profileData"])
async def removeurl(user: str, data: str):
    return None
