from typing import List

from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from iot_web.db.dependencies import get_db_session
from iot_web.web.api.user import schema
from iot_web.db.models.user import User


class UserDao:
    """Class for accessing user table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def create_user(self, user: schema.UserCreate) -> User:
        """
        Add user to database.
        """

        if await self.get_user_by_email(user.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exists.")

        # hash password.
        user.password = self.pwd_context.hash(user.password)
        new_user = User(**user.model_dump())
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)

        return new_user

    async def get_user_by_id(self, user_id: int) -> User:
        """Search for user in the database by id. If
        not found, return None.

        :param user_id: id of user to search for.
        :type user_id: int
        :return: found user or None.
        :rtype: User
        """

        query = select(User).where(User.id == user_id)
        rows = await self.session.execute(query)
        return rows.scalars().first()

    async def get_user_by_email(self, email: str) -> User:
        """Search for user in the database by email. If
        not found, return None.

        :param email: email of user to search for.
        :type email: str
        :return: found user or None.
        :rtype: User
        """

        query = select(User).where(User.email == email)
        rows = await self.session.execute(query)
        return rows.scalars().first()

    async def get_all_users(self, limit: int, offset: int) -> List[User]:
        """
        Get all dummy models with limit/offset pagination.

        :param limit: limit of dummies.
        :param offset: offset of dummies.
        :return: stream of dummies.
        """
        raw_dummies = await self.session.execute(
            select(User).limit(limit).offset(offset),
        )

        return list(raw_dummies.scalars().fetchall())

    async def update_user(self, updated_user: schema.UserCreate) -> User:
        """Update user in database.

        :param updated_user: new data from user
        :type updated_user: schema.UserCreate
        :raises HTTPException: HTTP 404 if user does not exist.
        :return: updated user.
        :rtype: User
        """

        # Return error if user does not exist.
        current_user = await self.get_user_by_email(updated_user.email)
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cannot update user that does not exist.")

        # Format user data.
        updated_user.password = self.pwd_context.hash(updated_user.password)
        updated_user.name = updated_user.name.lower()
        updated_user.last_name = updated_user.last_name.lower()

        # Update user.
        stmt = (
            update(User)
            .where(User.id == current_user.id)
            .values(**updated_user.model_dump())
        )
        updated_user = await self.session.execute(stmt)
        await self.session.commit()
        return current_user

    async def delete_user(self, user_id: int):
        """Delete user from database.

        :param user_id: id of user to delete.
        :type user_id: int
        :raises HTTPException: HTTP 404 if user does not exist.
        """
        # Return error if user does not exist.
        current_user = await self.get_user_by_id(user_id)
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cannot delete user that does not exist.")

        # Delete user.
        stmt = (
            delete(User).
            where(User.id == user_id)
        )
        await self.session.execute(stmt)
        await self.session.commit()
