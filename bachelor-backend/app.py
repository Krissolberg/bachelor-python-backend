from fastapi import FastAPI
import functions

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/shodansearch")
async def shodanUrlSearch():
    result = functions.shodanSearch('politiet.no')
    return result