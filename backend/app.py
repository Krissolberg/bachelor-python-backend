from typing import List
from fastapi import FastAPI, Query
import main as sho

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/shodansearch")
async def shodanSearch(URLs_and_IPs: List[str] = Query(None)):
    result = sho.sok(URLs_and_IPs)
    return result
