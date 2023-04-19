#!/bin/bash

mongoimport --jsonArray --db info_db --collection portDes --file /tmp/data/port.json
mongoimport --jsonArray --db info_db --collection leaderText --file /tmp/data/leader.json
mongoimport --jsonArray --db info_db --collection versionDes --file /tmp/data/versText.json
mongoimport --jsonArray --db info_db --collection vulnDes --file /tmp/data/vulns.json
mongoimport --jsonArray --db users --collection user --file /tmp/data/user.json