import pymongo
from pymongo.errors import PyMongoError

ip = "mongodb://localhost:27017/"


def mongoClient():
    return pymongo.MongoClient(ip)


def dbExist(db):
    try:
        with pymongo.timeout(5):
            dbnames = mongoClient().list_database_names()
            if db in dbnames:
                return True
            else:
                return False
    except:
        raise TypeError("Kunne ikke hente info")


def dbColExist(db, col):
    try:
        with pymongo.timeout(5):
            dbExist(db)
            mongoClient()[db].validate_collection(col)
            return True
    except:
        return False


def dbColDocuExist(db, col, navn):
    try:
        with pymongo.timeout(5):
            dbExist(db)
            dbColExist(db, col)
            if mongoClient()[db][col].count_documents({'navn': navn}, limit=1) != 0:
                return True
            else:
                return False
    except:
        return False