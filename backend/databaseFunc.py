import pymongo
import backend.apiExtentions.databaseCheck as dbCheck

client = dbCheck.mongoClient()


def verifyConnection():
    try:
        with pymongo.timeout(5):
            return client.server_info()
    except:
        return "Kunne ikke koble til database."


def getDatabases():
    try:
        with pymongo.timeout(5):
            return client.list_database_names()
    except:
        return "Kunne ikke koble til database."


def getCol(db):
    try:
        dbCheck.dbExist(db)
        return client[db].list_collection_names()
    except:
        return "Kunne ikke koble til database."


def getDataCol(db, col):
    try:
        if not dbCheck.dbExist(db):
            return "Databasen eksisterer ikke."
        if not dbCheck.dbColExist(db, col):
            return "Collection eksisterer ikke."
        return list(client[db][col].find({}, {"_id": 0}))
    except:
        return "Noe gikk galt."


def findDocu(db, navn):
    arr = {}
    try:
        if not dbCheck.dbExist(db):
            return "Databasen eksisterer ikke."
        allcol = getCol(db)
        for i in allcol:
            for ea in client[db][i].find({'navn': navn}, {'_id': 0}):
                arr[i] = ea
        return arr
    except:
        return "Noe gikk galt i søkingen."


def findOne(db, navn, col):
    try:
        if not dbCheck.dbExist(db):
            return "Databasen eksisterer ikke."
        return client[db][col].find_one({'navn': navn}, {'_id': 0})
    except:
        return "Noe gikk galt i søkingen."


def insertOne(db, col, navn, bes):
    try:
        if not dbCheck.dbExist(db):
            return "Databasen eksisterer ikke."
        if not dbCheck.dbColExist(db, col):
            return "Collection eksisterer ikke."
        if dbCheck.dbColDocuExist(db, col, navn):
            return "Dataen eksisterer allerede."
        client[db][col].update_one({
            'navn': navn
        },
            {
                '$setOnInsert': {'navn': navn, 'bes': bes}
            },
            upsert=True)
        return f'La inn {navn}: {bes} i {col}'
    except:
        return "Database og Collection eksisterer, men kunne ikke legge inn data."


def insertMany(db, col, navn, bes):
    for x in range(len(navn)):
        try:
            bes[x]
            insertOne(db, col, navn[x], bes[x])
            return "Lagt inn dataen som ikke fantes fra før."
        except IndexError:
            insertOne(db, col, navn[x], "")
            return "Lagt inn data uten beskrivelse."


def updateOne(db, col, navn, bes):
    try:
        if not dbCheck.dbExist(db):
            return "Databasen eksisterer ikke."
        if not dbCheck.dbColExist(db, col):
            return "Collection eksisterer ikke."
        if not dbCheck.dbColDocuExist(db, col, navn):
            return "Dataen eksisterer ikke."
        client[db][col].update_one({
            'navn': navn
        },
            {
                '$set': {'navn': navn, 'bes': bes}
            })
        return f'Oppdaterte {navn}: {bes} i {col}'
    except:
        return "Noe gikk galt."


def deleteOne(db, col, navn):
    try:
        if not dbCheck.dbExist(db):
            return "Databasen eksisterer ikke."
        if not dbCheck.dbColExist(db, col):
            return "Collection eksisterer ikke."
        if not dbCheck.dbColDocuExist(db, col, navn):
            return "Dataen eksisterer ikke."
        client[db][col].delete_one({'navn': navn})
        return f'Slettet {navn} fra {col} i {db}'
    except:
        return "Noe gikk galt."
