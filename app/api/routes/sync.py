import logging
from auth.jwt import get_current_user
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException

from app.config.mongo import source_collection
from app.utils.utils import convert_to_uppercase

# Initialize logger
logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/")
async def fetch_and_process_data(
    id: str,  # The ID of the document to fetch and process
    user_id: str = Depends(get_current_user)  # The ID of the user performing the action
):
    """
    Fetches a document from MongoDB, processes its data, and returns the processed data.

    Args:
        id (str): The ID of the document to fetch and process.
        user_id (str, optional): The ID of the user performing the action. Defaults to the ID of the current user.

    Raises:
        HTTPException: If the document with the given ID and user ID is not found.

    Returns:
        dict: A dictionary containing the ID of the document and the processed data.
    """

    # Fetch data from MongoDB based on document ID and user ID
    logger.info(f"Fetching data from MongoDB for document ID: {id}")
    document = await source_collection.find_one(
        {"_id": ObjectId(id), "user_id": user_id}
    )

    # Raise an exception if the document is not found
    if not document:
        logger.error(f"Document with ID: {id} not found for user ID: {user_id}")
        raise HTTPException(status_code=404, detail="Document not found")

    # Process the data
    # Convert all text fields in the document's 'source_data' field to uppercase
    logger.info(f"Converting text fields to uppercase for document ID: {id}")
    data_uppercase = convert_to_uppercase(document["source_data"])
    logger.info(f"Successfully processed data for document ID: {id}")
    # Return the document ID and the processed data
    return {"id": id, "processed_data": data_uppercase}
