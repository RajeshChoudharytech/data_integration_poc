import logging
from app.config.db import get_db
from auth.jwt import get_current_user
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.crud.destination_crud import CRUDDestination
from app.schema.models.models import ProcessedData

# Initialize logger
logger = logging.getLogger(__name__)
router = APIRouter()



@router.post("/")
async def register_destination(
    *,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user),
    id: str
) -> ProcessedData:  # The function returns an instance of ProcessedData
    """
    Register a new destination for processed data.

    This endpoint creates a new record in the ProcessedData table in the database.
    It takes the following parameters:

    - db: An instance of SQLAlchemy session.
    - user_id: The ID of the user.
    - id: The ID of the source data to be processed.

    Returns:
        An instance of ProcessedData.
    """
    # Log the start of the destination registration process
    logger.info(f"Starting registration of destination for user: {user_id} with source ID: {id}")

    # Create an instance of CRUDDestination with the ProcessedData table
    crud_destination = CRUDDestination(table=ProcessedData)

    try:
        # Create a new record in the ProcessedData table with the provided parameters
        result = await crud_destination.create(db=db, id=id, user_id=user_id)
        # Log successful registration
        logger.info(f"Destination registration successful for user: {user_id} with source ID: {id}")
        return result
    except Exception as e:
        # Log the exception with traceback
        logger.error(f"Error occurred during destination registration for user: {user_id} with source ID: {id}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")