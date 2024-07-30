import csv
import io

import logging
import requests
from auth.jwt import get_current_user
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.db import get_db
from app.config.mongo import source_collection
from app.schema.schema import Source

# Initialize logger
logger = logging.getLogger(__name__)
router = APIRouter()

destinations = {}

@router.post("/")
async def register_source(
    *,
    db: AsyncSession = Depends(get_db),  # Get a database session
    source: Source,  # The source data to be registered
    user_id: str = Depends(get_current_user)  # The ID of the user
):
    """
    Register a new source of data.

    This endpoint accepts either a URL or a file containing data to be registered.
    If a URL is provided, the data is fetched from the URL and stored in MongoDB.
    If a file is provided, the data is read from the file and stored in MongoDB.

    Args:
        db (AsyncSession): The database session.
        source (Source): The source data to be registered.
        user_id (str): The ID of the user.

    Returns:
        dict: A dictionary containing the ID of the registered source and the data.
    """

    logger.info(f"Registering source for user: {user_id}")

    if source.url:
        try:
            logger.info(f"Fetching data from URL: {source.url}")
            response = requests.get(source.url)
            response.raise_for_status()  # Raise an exception if the request fails
            data = response.json()  # Parse the response as JSON
            logger.info(f"Successfully fetched data from URL: {source.url}")
        except requests.RequestException as e:
            logger.error(f"Error fetching data from URL: {source.url}", exc_info=True)
            raise HTTPException(status_code=400, detail=f"Error fetching data from URL: {str(e)}")
    # checking if the file is provided
    elif source.file:
        try:
            logger.info("Reading data from file")
            contents = await source.file.read()
            data = []
            reader = csv.DictReader(io.StringIO(contents.decode('utf-8')))
            for row in reader:
                data.append(row)
            logger.info("Successfully read data from file")
        except Exception as e:
            logger.error("Error reading CSV file", exc_info=True)
            raise HTTPException(status_code=400, detail=f"Error reading CSV file: {str(e)}")
    else:
        logger.error("Neither URL nor file provided")
        raise HTTPException(status_code=400, detail="Either a URL or a file must be provided")

    try:
        logger.info("Storing data in MongoDB")
        result = await source_collection.insert_one({"user_id": user_id, "source_data": data})
        logger.info(f"Data stored successfully with ID: {result.inserted_id}")
    except Exception as e:
        logger.error("Error storing data in MongoDB", exc_info=True)
        raise HTTPException(status_code=500, detail="Error storing data in MongoDB")

    return {
        "id": str(result.inserted_id),  # Return the ID of the registered source
        "data": data  # Return the data
    }
