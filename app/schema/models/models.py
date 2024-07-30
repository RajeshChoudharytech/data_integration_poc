from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel
from sqlalchemy import Column, JSON


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True,  sa_column_kwargs={"unique": True})
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: str

class ProcessedData(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str
    source_id: str
    data: dict = Field(sa_column=Column(JSON))  
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
