from fastapi import FastAPI
import functions

print('Service mode enabled')
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/shodansearch")
async def shodan():
    result = functions.shodanSearch('politiet.no')
    return result