"""Defines the user API endpoints.
"""

from typing import List

import fastapi
from fastapi import APIRouter, Depends, status

from iot_web.db.dao.user_dao import UserDao
from iot_web.web.api.user import schema

ALL_USERS_LIMIT = 100


router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=schema.UserOut)
async def create_new_user(user: schema.UserCreate,
                          user_dao: UserDao = Depends()):
    """ Creates a new user in the database.
    """
    new_user = await user_dao.create_user(user)
    return new_user


@router.get("/{user_id}", response_model=schema.UserOut)
async def get_user(user_id: int, user_dao: UserDao = Depends()):
    """ Returns one user by id.
    """
    user = await user_dao.get_user_by_id(user_id)
    if not user:
        raise fastapi.HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="User not found.")
    return user


@router.get("/", response_model=List[schema.UserOut])
async def get_all_users(user_dao: UserDao = Depends()):
    """ Returns the first ALL_USERS_LIMIT of the user database.
    """
    users = await user_dao.get_all_users(ALL_USERS_LIMIT, 0)
    if not users:
        raise fastapi.HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="No users found.")
    return users


@router.put("/", status_code=status.HTTP_200_OK,
            response_model=schema.UserOut)
async def update_user(user_update: schema.UserCreate,
                      user_dao: UserDao = Depends()):
    """ Update a user in the database.
    """
    new_user = await user_dao.update_user(user_update)
    return new_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int,
                      user_dao: UserDao = Depends()):
    """ Delete a user in the database.
    """
    await user_dao.delete_user(user_id)
