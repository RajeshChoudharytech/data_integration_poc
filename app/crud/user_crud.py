from typing import Any

from auth.jwt import hash_password, verify_password
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.schema.schema import UserCreate


class CRUDUser:
    def __init__(self, table):
        self.table = table
        
    

    async def get(self, db: AsyncSession, id: Any):
        async with db.execute(select(self.table).where(self.table.id == id)) as result:
            return result.scalars().first()

    async def create(self, db: AsyncSession, *, obj_in: UserCreate):
        update_data = obj_in.dict(exclude_unset=True) if not isinstance(obj_in, dict) else obj_in

        # Check if the username already exists
        query = select(self.table).where(self.table.username == obj_in.username)
        result = await db.execute(query)
        existing_user = result.scalars().first()
        if existing_user:
            raise ValueError("Username already exists")

        # Hash the password before storing it
        if 'password' in update_data:
            update_data['password'] = hash_password(update_data['password'])
        db_obj = self.table(**update_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_by_username(self, db: AsyncSession, username: str):
        """
        Retrieve a user from the database by their username.

        Args:
            db (AsyncSession): The database session.
            username (str): The username of the user.

        Returns:
            The user object from the database, or None if not found.
        """
        # Construct the query to retrieve the user by username
        query = select(self.table).where(self.table.username == username)

        # Execute the query and get the result
        result = await db.execute(query)

        # Return the first user object (or None if not found)
        return result.scalars().first()

    async def authenticate(self, db: AsyncSession, username: str, password: str):
        """
        Authenticate a user by their username and password.

        Args:
            db (AsyncSession): The database session.
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            The user object if the authentication is successful, otherwise None.
        """
        # Retrieve the user from the database by their username
        user = await self.get_by_username(db, username)

        # Check if the user exists and if the password is correct
        if user and verify_password(password, user.password):
            return user

        # Return None if the authentication fails
        return None
