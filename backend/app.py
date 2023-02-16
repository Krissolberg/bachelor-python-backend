from typing import List, Union
from pydantic import BaseModel, Field
from fastapi import FastAPI, Query
import main as sho

app = FastAPI()

class Item(BaseModel):
    Field(default=None, example="noe")

@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/shodansearch")
async def shodanSearch(URLs_and_IPs: List[str] = Query(None)):
    result = sho.sok(URLs_and_IPs)
    return result

'''
Først, legg til Shodan API key i shodanFunc.py

For å kjøre må du ha uvicorn installert:
pip install -e .

Så kan du bruke:
uvicorn app:app

Så er det bare å gå til 127.0.0.1:8000/docs og prøve ut!

Merk: For nå så kan du ikke skrive inn dataen, dette jobbes på
'''