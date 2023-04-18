from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Optional, Dict
from uuid import uuid4
from passlib.context import CryptContext
import pickle
import os


class User(BaseModel):
    username: str
    email: Optional[str]
    password: str
    token: Optional[str]


class CreateUser(BaseModel):
    username: str
    email: Optional[str]
    password: str

users: Dict[str, User] = {}

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



def get_password_hash(password):
    return bcrypt_context.hash(password)


def get_user_securly(token: str):
    found_user = None

    for user in users:
        if user.token == token:
            found_user = user

    if found_user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials.")
    
    return found_user

def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)


@app.post("/create/user")
async def createNewUser(create_user: CreateUser):
    hash_password = get_password_hash(create_user.password)

    new_user = User(
        username=create_user.username,
        email=create_user.email,
        password=hash_password,
    )

    if new_user.email in users:
        raise HTTPException(status_code=422, detail="User with that e-mail already exists")
    
    users[new_user.email] = new_user

    return new_user


@app.post("/login")
async def login(email: str, password: str) -> str:
    print(users)

    # We use this check to make sure the user exists
    if email not in users:
        # We do not use 404 status code, because then we would reveil who has an account or not
        raise HTTPException(status_code=401, detail="Invalid credentials. Email not in user")
    
    user = users[email]

    # This is not needed because bcrypt has a verify check
    # hashed_password = get_password_hash(password)
    # print(hashed_password)
    # print(user)

    if not bcrypt_context.verify(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials. Hashed password not userpassword")

    # This method did not work because the hash is different for the same password due to salting
    # if hashed_password != user.password:
    #     raise HTTPException(status_code=401, detail="Invalid credentials. Hashed password not userpassword")
    
    token = uuid4()
    user.token = str(token)

    print(token)
    return token


@app.put("/user/update")
async def update(email: str, password: str, new_password: str) -> str:
    print(users)

    # We use this check to make sure the user exists
    if email not in users:
        # We do not use 404 status code, because then we would reveil who has an account or not
        raise HTTPException(status_code=401, detail="Invalid credentials. Email not in user")
    
    user = users[email]

    if not bcrypt_context.verify(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials. Hashed password not userpassword")
    
    new_hashed_password = get_password_hash(new_password)
    user.password = new_hashed_password

    return user

    




@app.get("/me")
async def get_me(user: User = Depends(get_user_securly)) -> User:
    return user