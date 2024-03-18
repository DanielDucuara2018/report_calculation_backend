from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from typing import Optional, Union

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from report_calculation.model import User as ModelUser
from report_calculation.schema import UserRequest as SchemaUserRequest
from report_calculation.utils import check_password_hash

logger = logging.getLogger(__name__)

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")

# create User


def create(user: SchemaUserRequest) -> ModelUser:
    logger.info("Adding new user")
    result = ModelUser(**dict(user)).create()
    logger.info("Added %s", result)
    return result


# delete User


def delete(user_id: str) -> ModelUser:
    logger.info("Deleting %s user", user_id)
    result = ModelUser.get(user_id=user_id).delete()
    logger.info("Deleted %s", result)
    return result


# get User


def read(user_id: Optional[str] = None, **kwargs) -> Union[ModelUser, list[ModelUser]]:
    if user_id:
        logger.info("Reading %s data", user_id)
        result = ModelUser.get(user_id=user_id)
    else:
        logger.info("Reading all data")
        result = ModelUser.find(**kwargs)
    logger.info("Result %s", result)
    return result


# update User


def update(user_id: str, data: SchemaUserRequest) -> ModelUser:
    logger.info("Updating %s with data %s", user_id, data)
    result = ModelUser.get(user_id=user_id).update(**dict(data))
    logger.info("Result %s", result)
    return result


# authenticate User


def authenticate_user(username: str, password: str) -> Optional[ModelUser]:
    users = read(username=username)
    if users and check_password_hash(users[0].password, password):
        return users[0]
    return None


# create User access token


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# get User for authentification


async def get_current_user(token: str = Depends(oauth2_scheme)) -> ModelUser:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise credentials_exception

    if not (username := payload.get("sub")):
        raise credentials_exception

    users = read(username=username)
    if not users:
        raise credentials_exception
    return users[0]
