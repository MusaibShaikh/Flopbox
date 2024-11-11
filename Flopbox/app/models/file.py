from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FileBase(BaseModel):
    Filename: str
    FilePath: str
    FileType: str
    Comment: Optional[str] = None  

class FileCreate(FileBase):
    UserId: str 

class FileResp(FileBase):
    Id: str
    MD5Hash: str
    UploadDate: datetime
