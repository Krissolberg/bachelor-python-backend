<!-- KOMME I GANG -->
## Komme i gang

For å komme i gang og kjøre prosjektet lokalt så følger du disse trinnene.

### Forutsetninger

Prosjektet er under utvikling, dermed er det veldig viktig å sjekke om alt du trenger er installert.
Du må ha Python3 installert og den nyeste Python3 pip. Installeringen under gjelder for Ubuntu basert datamaskiner.

```sh
sudo apt update -y
sudo apt install python3-pip -y
sudo -H pip install --upgrade pip
sudo apt install git -y
```

### Installering

1. Klon repo-et
   ```sh
   git clone https://github.com/Krissolberg/bachelor-python-backend.git
   ```
2. Legg til API-key fra [Shodan](https://account.shodan.io/) i [shodanService](backend/apiExtentions/shodanGetService.py)
3. Kjør [installDocker.sh](docker/installDocker.sh)
   ```sh
   sudo su
   chmod 700 docker/installDocker.sh
   ./docker/installDocker.sh -y
   ```
4. Initialiser databasen
   ```sh
   sudo docker compose -f docker/docker-compose.yml up -d
   ```
5. Kjør webserveren
   ```sh
   uvicorn main:app
   ```
6. Sjekk dokumentasjonen i [webserveren](http://127.0.0.1:8000/docs)

#### Alternativ kjøring av webserver
* ```sh
   uvicorn main:app --reload
   ```
* ```sh
   uvicorn main:app --reload --host 0.0.0.0 --port 80
   ```

<!-- BRUK AV API -->
## Eksempler på bruk av API

### /search || /single
* url (oslomet.no, www.oslomet.no...)
* ip (192.168.1.1, 0.0.0.0...)
* iprange (0.0.0.0-1.2.3.4, 1.1.1.1-2.2.2.2)


<!-- Cool to know -->
### Tankegang
ShodanFunksjonen bruker regex til å filtrere IP og IP-range, dette blir deretter trukket fra inndata. Og da har vi kun URL.
Søken starter med å legge inn hver IP fra IP-range (med multithreading), så bruker vi Shodan til å finne IP fra URL og legger alt i en samlet IP-liste.

Deretter brukes det multithreading for å gå gjennom hver IP og sende dette til Shodan-API. Cachingen lytter etter hver "post"-kall som gjøres og lagrer dataen som kommer fra dette. Her vil også IP-er som ikke finnes også bli lagret.

Hvis samme søk gjøres igjen, så vil det igjen brukes multithreading for å gå gjennom IP-listen, men denne gang så hentes det data fra cache. Noe som vil bemerkes fra hastigheten.

Cache-en er koblet opp til en lokal MongoDB.