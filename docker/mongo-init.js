const ports = require('port.json');
const versi = require('versTekst.json');
const vuln = require('vulns.json');
const leder = require('leder.json');

db = db.getSiblingDB('info_db');

db.createCollection('portBes');
db.createCollection('versionBes');
db.createCollection('vulnBes');
db.createCollection('lederTekst');

db.portBes.insertMany(ports);

db.versionBes.insertMany(versi);

db.vulnBes.insertMany(vuln);

db.lederTekst.insertMany(leder);