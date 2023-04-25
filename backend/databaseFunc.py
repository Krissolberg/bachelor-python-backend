from datetime import datetime

from pymongo import timeout
import backend.apiExtentions.databaseCheck as dbCheck
from backend.apiExtentions.databaseCheck import mongoClient

client = mongoClient()

timestamp = datetime.utcnow()
date = timestamp.strftime("%d-%m-%Y")
time = timestamp.strftime("%H:%M:%S")


def verifyConnection():
    try:
        with timeout(5):
            return client.server_info()
    except:
        return "Could not reach MongoDB. Is MongoDB running?"


def getDatabases():
    try:
        with timeout(5):
            return client.list_database_names()
    except:
        return "Could not reach MongoDB. Is MongoDB running?"


def getCol(db):
    try:
        dbCheck.dbExist(db)
        return client[db].list_collection_names()
    except:
        return "Could not reach MongoDB. Is MongoDB running?"


def getDataCol(db, col):
    try:
        if not dbCheck.dbExist(db):
            return "Database does not exist."
        if not dbCheck.dbColExist(db, col):
            return "Collection does not exist."
        return list(client[db][col].find({}, {"_id": 0}))
    except:
        return "Could not reach MongoDB. Is MongoDB running?"


def findDocu(db, name):
    arr = {}
    temp = {}
    try:
        if not dbCheck.dbExist(db):
            return "Database does not exist."
        allcol = getCol(db)
        for i in allcol:
            temp[i] = [ea for ea in client[db][i].find({'name': name}, {'_id': 0})]
            if temp[i]:
                arr[i] = temp[i]
        return arr
    except:
        return "Something unexpected happened while searching."


def findOne(db, key, name, col):
    try:
        if not dbCheck.dbExist(db):
            return "Database does not exist."
        return client[db][col].find_one({f'{key}': name}, {'_id': 0})
    except:
        return "Something unexpected happened while searching."


def insertOne(db, col, name, des):
    try:
        if not dbCheck.dbExist(db):
            return "Database does not exist."
        if not dbCheck.dbColExist(db, col):
            return "Collection does not exist."
        if dbCheck.dbColDocuExist(db, col, "name", name):
            return "Name already exists."
        client[db][col].update_one({
            'name': name
        },
            {
                '$setOnInsert': {'name': name, 'des': des}
            },
            upsert=True)
        return f'La inn {name}: {des} i {col}'
    except:
        return "Something unexpected happened. Database and Collection exists, but could not insert data."


def insertMany(db, col, name, des):
    for x in range(len(name)):
        try:
            insertOne(db, col, name[x], des[x])
            return "Inserted data that did not exist."
        except IndexError:
            insertOne(db, col, name[x], "")
            return "Inserted data without description."


def updateOne(db, col, name, des):
    try:
        if not dbCheck.dbExist(db):
            return "Database does not exist."
        if not dbCheck.dbColExist(db, col):
            return "Collection does not exist."
        if not dbCheck.dbColDocuExist(db, col, "name", name):
            return "Data does not exist."
        client[db][col].update_one({
            'name': name
        },
            {
                '$set': {'name': name, 'des': des}
            })
        return f'Updated, {name}. With the description; {des}.'
    except:
        return "Something unexpected happened. Database and Collection exists, but could not update data."


def deleteOne(db, col, name):
    try:
        if not dbCheck.dbExist(db):
            return "Database does not exist."
        if not dbCheck.dbColExist(db, col):
            return "Collection does not exist."
        if not dbCheck.dbColDocuExist(db, col, "name", name):
            return "Data does not exist."
        client[db][col].delete_one({'name': name})
        return f'Successfully removed, {name}.'
    except:
        return "Something unexpected happened. Database and Collection exists, but could not delete data."


def tls_statement(versions_count):
    totalOldVersions, search = False, ""
    try:
        tls_1_2 = versions_count['TLSv1.2']
    except:
        tls_1_2 = 0
    try:
        tls_1_3 = versions_count['TLSv1.3']
    except:
        tls_1_3 = 0
    for key, value in versions_count.items():
        if key != "TLSv1.3" and key != "TLSv1.2":
            totalOldVersions = True
            break

    if tls_1_2 == tls_1_3:
        search = "1.2and1.3"
    elif tls_1_2 and tls_1_3 == 0:
        search = "1.2"
    elif tls_1_3 and tls_1_2 == 0:
        search = "1.3"
    elif tls_1_2 > tls_1_3:
        search = "1.2some1.3"
    if totalOldVersions:
        search = search + "withold"

    try:
        return findOne("info_db", "name", search, "versionDes")['des']
    except:
        return f'Found no match of: {search}, in database.'


'''*************** Login functions *************'''


def findOneWithID(db, key, name, col):
    try:
        if not dbCheck.dbExist(db):
            return "Database does not exist."
        return client[db][col].find_one({f'{key}': name})
    except:
        return "Something unexpected happened while searching."


def insertUser(db, col, username, email, password, role):
    try:
        if not dbCheck.dbExist(db):
            return "Database does not exist."
        if not dbCheck.dbColExist(db, col):
            return "Collection does not exist."
        client[db][col].update_one({
            'email': email
        },
            {
                '$setOnInsert': {'username': username, 'role': role, 'email': email, 'password': password, 'logSearch': {},
                                 'savedSearch': []}
            },
            upsert=True)
        client[db]["tokens"].create_index("expiration", expireAfterSeconds=43200)
        client[db]["tokensLong"].create_index("expiration", expireAfterSeconds=172800)
        return f'La inn {username}: {email} i {col}'
    except:
        return "Something unexpected happened. Database and Collection exists, but could not insert data."


def updatePassword(email, newpassword):
    try:
        if not dbCheck.dbExist("users"):
            return "Database does not exist."
        if not dbCheck.dbColExist("users", "user"):
            return "Collection does not exist."
        try:
            user = findOneWithID("users", "email", email, "user")
        except:
            return "Could not find user"
        client["users"]["user"].update_one({
            'user': user["_id"]
        },
            {
                '$set': {'password': newpassword}
            }, upsert=True)
        return 'Password updated.'
    except:
        return "Something unexpected happened. Database and Collection exists, but could not update data."


def updateToken(db, email, token, remember):
    col = "tokensLong" if remember else "tokens"
    try:
        if not dbCheck.dbExist(db):
            return "Database does not exist."
        if not dbCheck.dbColExist(db, col):
            return "Collection does not exist."
        try:
            user = findOneWithID("users", "email", email, "user")
        except:
            return "Could not find user"
        client[db][col].update_one({
            'user': user["_id"]
        },
            {
                '$set': {'token': token, 'expiration': timestamp}
            }, upsert=True)
        return 'Token updated.'
    except:
        return "Something unexpected happened. Database and Collection exists, but could not update data."


def saveSearch(db, col, tokenID, array):
    try:
        if not dbCheck.dbExist(db):
            return "Database does not exist."
        if not dbCheck.dbColExist(db, col):
            return "Collection does not exist."
        user = findOneWithID("users", "_id", tokenID['user'], "user")
        client[db][col].update_one({
            '_id': user['_id']
        },
            {
                '$set': {f'logSearch.{date}.{time}': array}
            },
            upsert=True)
        ea = []
        user = findOneWithID("users", "_id", tokenID['user'], "user")
        for key, value in user['logSearch'].items():
            for key1, value1 in value.items():
                for value2 in value1:
                    if value2 not in ea:
                        ea.append(value2)
        client[db][col].update_one({
            '_id': user['_id']
        },
            {
                '$set': {'savedSearch': ea}
            },
            upsert=True)
        return True
    except:
        return False


def removeSearch(db, col, tokenID, array):
    try:
        if not dbCheck.dbExist(db):
            return "Database does not exist."
        if not dbCheck.dbColExist(db, col):
            return "Collection does not exist."
        user = findOneWithID("users", "_id", tokenID['user'], "user")
        if user["savedSearch"]:
            tempSave = []
            for value in user["savedSearch"]:
                if value not in array:
                    tempSave.append(value)
            client[db][col].update_one({
                '_id': user['_id']
            },
                {
                    '$set': {'savedSearch': tempSave}
                },
                upsert=True)
        return True
    except:
        return False
