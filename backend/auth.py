from fastapi import HTTPException
from uuid import uuid4
from passlib.context import CryptContext
from backend.databaseFunc import insertUser, findOne, updateToken, saveSearch, updatePassword, removeSearch
from backend.apiExtentions.databaseCheck import dbColDocuExist

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def createNewUser(username, email, passord):
    if dbColDocuExist("users", "user", "email", email):
        raise HTTPException(status_code=422, detail="User with that e-mail already exists")

    return insertUser("users", "user", username, email, bcrypt_context.hash(passord))


def userLogin(email: str, password: str, remember: bool):
    if not dbColDocuExist("users", "user", "email", email):
        raise HTTPException(status_code=401, detail="Invalid credentials. Email not in user")

    user = findOne("users", "email", email, "user")

    if not bcrypt_context.verify(password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials. Hashed password not userpassword")

    token = uuid4()
    updateToken('users', email, str(token), remember)
    return token


def updateUserPassword(email: str, password: str, new_password: str) -> str:
    # We use this check to make sure the user exists
    if not dbColDocuExist("users", "user", "email", email):
        # We do not use 404 status code, because then we would reveil who has an account or not
        raise HTTPException(status_code=401, detail="Invalid credentials. Email not in user")

    user = findOne("users", "email", email, "user")

    if not bcrypt_context.verify(password, user['password']):
        raise HTTPException(status_code=401, detail="Invalid credentials. Hashed password not userpassword")

    return updatePassword(email, bcrypt_context.hash(new_password))


def getUserinfo(token: str):
    firstFind = findOne("users", "token", token, "tokens")
    secondFind = findOne("users", "token", token, "tokensLong")
    if firstFind:
        return findOne("users", "_id", firstFind['user'], "user")
    elif secondFind:
        return findOne("users", "_id", secondFind['user'], "user")
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials. Token is not valid")


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
        raise HTTPException(status_code=401, detail="Invalid credentials. Token is not valid")


def validToken(token: str):
    if findOne("users", "token", token, "tokens"):
        return True
    elif findOne("users", "token", token, "tokensLong"):
        return True
    else:
        return HTTPException(status_code=401, detail="Invalid credentials. Token is not valid")
