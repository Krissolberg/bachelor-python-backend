from fastapi import HTTPException
from uuid import uuid4
from passlib.context import CryptContext
from backend.databaseFunc import insertUser, findOne, updateToken
from backend.apiExtentions.databaseCheck import dbColDocuExist

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def createNewUser(username, email, passord):
    hash_password = bcrypt_context.hash(passord)

    if dbColDocuExist("users", "user", "email", email):
        raise HTTPException(status_code=422, detail="User with that e-mail already exists")

    return insertUser("users", "user", username, email, hash_password)


def userLogin(email: str, password: str):
    # We use this check to make sure the user exists
    if not dbColDocuExist("users", "user", "email", email):
        # We do not use 404 status code, because then we would reveil who has an account or not
        raise HTTPException(status_code=401, detail="Invalid credentials. Email not in user")

    user = findOne("users", "email", email, "user")

    # This is not needed because bcrypt has a verify check
    # hashed_password = get_password_hash(password)
    # print(hashed_password)
    # print(user)

    if not bcrypt_context.verify(password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials. Hashed password not userpassword")

    # This method did not work because the hash is different for the same password due to salting
    # if hashed_password != user.password:
    #     raise HTTPException(status_code=401, detail="Invalid credentials. Hashed password not userpassword")

    token = uuid4()

    updateToken('users', 'user', user['username'], user['email'], user['password'], str(token))

    return token


def updateUserPassword(email: str, password: str, new_password: str) -> str:
    # We use this check to make sure the user exists
    if not dbColDocuExist("users", "user", "email", email):
        # We do not use 404 status code, because then we would reveil who has an account or not
        raise HTTPException(status_code=401, detail="Invalid credentials. Email not in user")

    user = findOne("users", "email", email, "user")

    if not bcrypt_context.verify(password, user['password']):
        raise HTTPException(status_code=401, detail="Invalid credentials. Hashed password not userpassword")

    new_hashed_password = bcrypt_context.hash(new_password)
    updateToken('users', 'user', user['username'], user['email'], new_hashed_password, user['token'])

    return user


def getUserinfo(token: str):
    return findOne("users", "token", token, "user")
