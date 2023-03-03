# Python backend for Bachelor prosjektet

Start med å legge inn Shodan API key i backend/apiExtentions/shodanGetService

For å kjøre så må du ha alle nødvendige pakker installert:
pip install -e .

For å kjøre fastAPI med Uvicorn:
uvicorn main:app

Optional (hvis du ønsker autoReload):
uvicorn main:app --reload

Nå vil du se i localhost:8000/docs at det ligger API kall