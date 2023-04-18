#!/bin/bash

mongoimport --jsonArray --db info_db --collection portBes --file /tmp/data/port.json
mongoimport --jsonArray --db info_db --collection lederTekst --file /tmp/data/leder.json
mongoimport --jsonArray --db info_db --collection versionBes --file /tmp/data/versTekst.json
mongoimport --jsonArray --db info_db --collection vulnBes --file /tmp/data/vulns.json
mongoimport --jsonArray --db users --collection user --file