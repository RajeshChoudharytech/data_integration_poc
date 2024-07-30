
from bson import ObjectId
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.mongo import source_collection
from app.schema.models.models import ProcessedData
from app.utils.utils import convert_to_uppercase


class CRUDDestination:
    def __init__(self, table):
        self.table = table
        
    
    async def create(self, db: AsyncSession, *, id: str, user_id: str):
        # Fetch data from MongoDB based on the provided source_id
        document = await source_collection.find_one({"_id": ObjectId(id), "user_id": user_id})

        if not document:
            raise HTTPException(status_code=404, detail="Document not found")

        # Process the data by converting all text fields to uppercase
        data_uppercase = convert_to_uppercase(document["source_data"])

        # Store the processed data in SQLite
        processed_data = ProcessedData(
            user_id=user_id,
            source_id=id,
            data=data_uppercase  # Store the JSON data directly
        )

        try:
            db.add(processed_data)
            await db.commit()
            await db.refresh(processed_data)
        except IntegrityError:
            await db.rollback()
            raise HTTPException(status_code=500, detail="Error storing processed data")

        return {"destination_id": processed_data.id, "data": data_uppercase}
