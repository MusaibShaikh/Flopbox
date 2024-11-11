from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    Username: str
    Email: EmailStr

class UserCreate(UserBase):
    Password: str  

class UserResponse(UserBase):
    Id: str
    Files: List['FileResponse'] = []  

class UserWithPasswordHash(UserBase):
    Salt: str
    PasswordHash: str
