from pymongo import MongoClient, timeout

ip = "mongodb://localhost:27017/"


def mongoClient():
    return MongoClient(ip)


def dbExist(db):
    try:
        with timeout(5):
            dbnames = mongoClient().list_database_names()
            if db in dbnames:
                return True
            else:
                return False
    except:
        raise TypeError("Kunne ikke hente info")


def dbColExist(db, col):
    try:
        with timeout(5):
            dbExist(db)
            mongoClient()[db].validate_collection(col)
            return True
    except:
        return False


def dbColDocuExist(db, col, key, navn):
    try:
        with timeout(5):
            dbExist(db)
            dbColExist(db, col)
            if mongoClient()[db][col].count_documents({f'{key}': navn}, limit=1) != 0:
                return True
            else:
                return False
    except:
        return False
