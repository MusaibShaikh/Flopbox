from sqlalchemy.orm import Session
from models.models import User
from fastapi import HTTPException
import bcrypt
import os
from models.user import UserCreate
import logging
import uuid

logger = logging.getLogger(__name__)

class UserService:

    @staticmethod
    def generate_salt() -> str:
        # Generate a 16-byte salt
        return os.urandom(16).hex()

    @staticmethod
    def get_password_hash(password: str, salt: str) -> str:
        # Use the salt with bcrypt to hash the password
        salted_password = f"{salt}{password}".encode()  # Combine salt and password
        return bcrypt.hashpw(salted_password, bcrypt.gensalt()).decode()

    @staticmethod
    def verify_password(plain_password: str, salt: str, hashed_password: str) -> bool:
        # Combine the salt with the provided plain password and verify against the stored hash
        salted_password = f"{salt}{plain_password}".encode()
        return bcrypt.checkpw(salted_password, hashed_password.encode())

    @staticmethod
    def create_user(db: Session, user: UserCreate):
        # Check if username or email already exists
        existing_user = db.query(User).filter((User.Username == user.Username) | (User.Email == user.Email)).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username or email already exists.")

        # Generate a unique salt and hash the password with it
        salt = UserService.generate_salt()
        hashed_password = UserService.get_password_hash(user.Password, salt)

        # Create a new User instance
        new_user = User(Username=user.Username, Email=user.Email, Salt=salt, PasswordHash=hashed_password, Id = uuid.uuid4() )
        db.add(new_user)

        try:
            db.commit()
            db.refresh(new_user)
            return True
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def authenticate_user(db: Session, username: str, password: str):
        # Fetch the user by username
        user = db.query(User).filter(User.Username == username).first()
        if not user:
            return False

        # Verify the provided password using the user's stored salt and hashed password
        if UserService.verify_password(password, user.Salt, user.PasswordHash):
            return user
        return False
