db = db.getSiblingDB('info_db');

db.createCollection('portBes');
db.createCollection('versionsBes');
db.createCollection('vulnsBes');

db.portBes.insertMany([
 {
    port: '8080',
    beskrivelse: 'noe',
    addrs: 'mer info?'
  },
  {
    port: '80',
    filter: 'noe annet',
    addrs: 'mer info?'
  }
]);

db.versionsBes.insertMany([
 {
    port: '-TLSv1',
    beskrivelse: 'noe',
    addrs: 'mer info?'
  }
]);

db.vulnsBes.insertMany([
 {
    port: 'CVE',
    beskrivelse: 'noe',
    addrs: 'mer info?'
  }
]);

