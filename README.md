# Python backend for Bachelor prosjektet

Start med å legge inn API key i backend/shodanFunc.py

For å kjøre så må du ha alle nødvendige pakker installert:
pip install -e .

For å kjøre fastAPI med Uvicorn så navigerer du deg til backend mappen, også kjører:
uvicorn app:app

Optional (hvis du ønsker autoReload):
uvicorn app:app --reload

Nå vil du se i localhost:8000/docs at det ligger API kall
