from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from app.config.base import settings
import jwt

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Initialize password context for hashing passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create an access token for authentication.

    Args:
        data (dict): Data to be encoded in the token.
        expires_delta (Optional[timedelta]): Time until the token expires.
            Defaults to None.

    Returns:
        str: The encoded access token.
    """
    # Create a copy of the data to avoid modifying the original
    to_encode = data.copy()

    # Calculate the expiration time
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # Encode the data in the token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a refresh token for authentication.

    Args:
        data (dict): Data to be encoded in the token.
        expires_delta (Optional[timedelta]): Time until the token expires.
            Defaults to None.

    Returns:
        str: The encoded refresh token.
    """
    # Create a copy of the data to avoid modifying the original
    to_encode = data.copy()

    # Calculate the expiration time
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    # Add the expiration time to the data
    to_encode.update({"exp": expire})

    # Encode the data in the token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt



def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify if a plain password matches a hashed password.

    Args:
        plain_password (str): The plain password to be verified.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the plain password matches the hashed password, False otherwise.
    """
    # Use the password context to verify if the plain password matches the hashed password
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str) -> str:
    """
    Hashes the given password using the password context.

    Args:
        password (str): The password to be hashed.

    Returns:
        str: The hashed password.
    """
    # Use the password context to hash the password
    return pwd_context.hash(password)



def decode_jwt(token: str) -> dict:
    """
    Decodes a JWT token and returns the payload.

    Args:
        token (str): The JWT token to decode.

    Raises:
        HTTPException: If the token has expired or is invalid.

    Returns:
        dict: The payload of the JWT token.
    """
    try:
        # Decode the token using the secret key and specified algorithm
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        # Raise an HTTPException if the token has expired
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.PyJWTError:
        # Raise an HTTPException if the token is invalid
        raise HTTPException(status_code=401, detail="Invalid token")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Get the current user from the token.

    Args:
        token (str, optional): The token to decode. Defaults to the token from the authorization header.

    Raises:
        HTTPException: If the token has expired or is invalid.
        HTTPException: If the token is missing or invalid.
        HTTPException: If there is an error validating the token.

    Returns:
        str: The user ID extracted from the token.
    """
    try:
        # Decode the token to get the user info
        payload = decode_jwt(token)
        
        # Extract the user ID from the payload
        user_id = payload.get("sub")  # Adjust according to how you store user info in the token
        
        # Raise an error if the user ID is missing
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        
        # Return the user ID
        return user_id
    
    # Raise an error if the token has expired
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    
    # Raise an error if the token is invalid
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    # Raise an error if there is an error validating the token
    except Exception:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
