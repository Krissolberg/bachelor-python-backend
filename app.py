from fastapi import FastAPI
import main as faen

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/shodansearch")
async def shodanUrlSearch():
    result = faen.sok(['politiet.no'])
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