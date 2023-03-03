from typing import List
from fastapi import FastAPI, Query, Header
import shodanFunc as sho

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
        "name": "profile",
        "description": "Login/Register/Forgot"
    },
    {
        "name": "profileData",
        "description": "Saved IPs/Url"
    },
]

app = FastAPI(openapi_tags=tags_metadata)


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/search", tags=["shodan"])
async def shodan_search(url_ip: List[str] = Query(...)):
    return sho.sok(url_ip)


# ... er det samme som Required fra pydantic

@app.get("/single", tags=["shodan"])
async def single_search(url_ip: str = Query(...)):
    return sho.sok([url_ip])


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
