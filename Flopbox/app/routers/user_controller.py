from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from models.db_context import DbObject
from handlers.user_service import UserService
from models.user import UserCreate
import logging

router = APIRouter()
db_context = DbObject()
db_context.CreateConnection("mysql+pymysql://root:ororZZKkPTnvAPsrdXHDKuUjEsfSSOiQ@junction.proxy.rlwy.net:28681/railway")
_current_db_session = db_context.GetCurrentSession()

logger = logging.getLogger(__name__)
@router.post("/user/")
def register_user(user : UserCreate):
    return UserService.create_user(_current_db_session, user)

@router.post("/login/")
def login(username: str = Body(...), password: str = Body(...)):
    user = UserService.authenticate_user(_current_db_session, username, password)
    if not user:
        raise HTTPException(status_code=401, detail="incorrect username or password")
    return {"message": "user authenticated successfully"}
