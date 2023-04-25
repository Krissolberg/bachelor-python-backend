from fastapi import HTTPException
from uuid import uuid4
from passlib.context import CryptContext
from backend.databaseFunc import insertUser, findOne, updateToken, saveSearch, updatePassword, removeSearch
from backend.apiExtentions.databaseCheck import dbColDocuExist

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def createNewUser(username, role, email, password):
    username, email = username.lower(), email.lower()
    if dbColDocuExist("users", "user", "email", email):
        raise HTTPException(status_code=422, detail="User with that e-mail already exists.")
    if dbColDocuExist("users", "user", "username", username):
        raise HTTPException(status_code=422, detail="User with that username already exists.")
    if len(password) < 3:
        raise HTTPException(status_code=406, detail="Password has to be atleast 3 characters.")

    return insertUser("users", "user", username, role, email, bcrypt_context.hash(password))


def userLogin(emailorusername: str, password: str, remember: bool):
    emailorusername = emailorusername.lower()
    if dbColDocuExist("users", "user", "email", emailorusername):
        key = "email"
    elif dbColDocuExist("users", "user", "username", emailorusername):
        key = "username"
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials. Email/Username does not exist.")

    user = findOne("users", key, emailorusername, "user")

    if not bcrypt_context.verify(password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials. Wrong password.")

    token = uuid4()
    updateToken('users', emailorusername, str(token), remember)
    return token


def updateUserPassword(email: str, password: str, new_password: str) -> str:
    email = email.lower()

    if len(new_password) < 3:
        raise HTTPException(status_code=406, detail="New password has to be atleast 3 characters.")

    if not dbColDocuExist("users", "user", "email", email):
        raise HTTPException(status_code=401, detail="Invalid credentials. Email does not exist.")

    user = findOne("users", "email", email, "user")

    if not bcrypt_context.verify(password, user['password']):
        raise HTTPException(status_code=401, detail="Invalid credentials. Wrong password.")

    return updatePassword(email, bcrypt_context.hash(new_password))


def getUserinfo(token: str):
    firstFind = findOne("users", "token", token, "tokens")
    secondFind = findOne("users", "token", token, "tokensLong")
    if firstFind:
        return findOne("users", "_id", firstFind['user'], "user")
    elif secondFind:
        return findOne("users", "_id", secondFind['user'], "user")
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials. Token is not valid.")


def updateSavedSearch(token: str, array):
    firstFind = findOne("users", "token", token, "tokens")
    secondFind = findOne("users", "token", token, "tokensLong")
    if firstFind:
        return saveSearch("users", "user", firstFind, array)
    elif secondFind:
        return saveSearch("users", "user", secondFind, array)
    else:
        raise HTTPException(status_code=400, detail="Could not save log.")


def removeSavedSearch(token: str, removeArray):
    firstFind = findOne("users", "token", token, "tokens")
    secondFind = findOne("users", "token", token, "tokensLong")
    if firstFind:
        return removeSearch("users", "user", firstFind, removeArray)
    elif secondFind:
        return removeSearch("users", "user", secondFind, removeArray)
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials. Token is not valid.")


def validToken(token: str):
    if findOne("users", "token", token, "tokens"):
        return True
    elif findOne("users", "token", token, "tokensLong"):
        return True
    else:
        return HTTPException(status_code=401, detail="Invalid credentials. Token is not valid.")
