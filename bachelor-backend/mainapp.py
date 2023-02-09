import sys
import functions
from fastapi import FastAPI, Request

print('Service mode enabled')
app = FastAPI()

@app.get("/")
async def root():
    # return {"message": "Hello World"}
    return {"message"}
    


@app.get("/shodan")
async def readShodan():
    # return functions.shodanSearch(input)
    return functions.shodanSearch('politiet.no')
    


# IP = functions.shodanSearch(input)
# print(IP)

# for i in IP:
#     functions.shodanHost(i)
