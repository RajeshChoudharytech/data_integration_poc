
from auth.jwt import create_access_token, create_refresh_token
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.db import get_db
from app.crud.user_crud import CRUDUser
from app.schema.models.models import User
from app.schema.schema import UserCreate, UserLogin

router = APIRouter()

crud_user = CRUDUser(table=User)



@router.post("/")
async def user_signup(*, db: AsyncSession = Depends(get_db), payload: UserCreate):
    """
    Sign up a new user.

    Args:
        db (AsyncSession): The database session.
        payload (UserCreate): The user data to be created.

    Returns:
        dict: The serialized user object.

    Raises:
        HTTPException: If there is an error creating the user.
    """
    try:
        # Create a new user in the database
        user = await crud_user.create(db=db, obj_in=payload)

        # Serialize the user object
        return jsonable_encoder(user)
    except ValueError as e:
        # Raise an exception if there is a validation error
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Raise an exception if there is an unexpected error
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/login")
async def user_login(user_login: UserLogin, db: AsyncSession = Depends(get_db)):
    """
    Authenticate a user and return JWT tokens.

    Args:
        user_login (UserLogin): The user's login credentials.
        db (AsyncSession, optional): The database session. Defaults to Depends(get_db).

    Returns:
        dict: A dictionary containing the access token and refresh token.

    Raises:
        HTTPException: If the user's credentials are invalid.
    """
    # Create a CRUD object for the User model
    crud_user = CRUDUser(table=User)
    
    # Authenticate the user using the CRUD object
    user = await crud_user.authenticate(db, user_login.username, user_login.password)
    
    # If the user is not authenticated, raise an exception
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Create access and refresh tokens
    access_token = create_access_token(data={"sub": user_login.username})
    refresh_token = create_refresh_token(data={"sub": user_login.username})
    
    # Return the tokens in a dictionary
    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }
