from typing import Optional

from fastapi import UploadFile
from pydantic import BaseModel, HttpUrl


class Source(BaseModel):
    url: Optional[HttpUrl] = None
    file: Optional[UploadFile] = None

class SyncRequest(BaseModel):
    source_id: str
    destination_id: str
    


class UserCreate(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str
    
class UserLogin(BaseModel):
    username: str
    password: str


class UserRead(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str

    class Config:
        orm_mode = True
