from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.models import File, User
import hashlib
import datetime
import os
from loguru import logger
import uuid

UPLOAD_DIRECTORY = "uploads"
ALLOWED_EXTENSIONS = {".zip", ".mp4", ".mov", ".avi", ".txt", ".pdf", ".jpg", ".png", ".json"}

class FileService:

    @staticmethod
    def compute_md5(file_content: bytes) -> str:
        md5 = hashlib.md5()
        md5.update(file_content)
        return md5.hexdigest()

    @staticmethod
    def get_file_extension(filename: str) -> str:
        _, ext = os.path.splitext(filename)
        return ext.lower()

    @staticmethod
    def get_unique_filename(filename: str) -> str:
        file_path = os.path.join(UPLOAD_DIRECTORY, filename)
        if not os.path.exists(file_path):
            return filename

        name, ext = os.path.splitext(filename)
        counter = 1

        while os.path.exists(file_path):
            new_filename = f"{name}({counter}){ext}"
            file_path = os.path.join(UPLOAD_DIRECTORY, new_filename)
            counter += 1

        return new_filename

    @staticmethod
    async def upload_file(file_content: bytes, filename: str, user_id: str, comment: str, db: Session):
        # Check if user exists
        user = db.query(User).filter(User.Id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
    
        # Check if the file type is allowed
        file_extension = FileService.get_file_extension(filename)
        if file_extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(status_code=400, detail=f"File type '{file_extension}' is not allowed.")
    
        # Compute MD5 hash of file content
        md5_hash = FileService.compute_md5(file_content)
    
        # Get a unique filename if the same filename already exists
        unique_filename = FileService.get_unique_filename(filename)
        file_path = os.path.join(UPLOAD_DIRECTORY, unique_filename)
    
        # Save the file content to the filesystem
        try:
            with open(file_path, "wb") as f:
                f.write(file_content)
        except Exception as e:
            logger.error(f"Failed to save file to filesystem: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to save file on the server.")
    
        # Create a new File record in the database
        new_file = File(
            Filename=unique_filename,
            FilePath=file_path,
            FileType=file_extension,
            MD5Hash=md5_hash,
            UploadDate=datetime.datetime.utcnow(),
            UserId=user_id,
            Comment=comment,
            Id = uuid.uuid4()
        )
    
        try:
            db.add(new_file)
            db.commit()
            db.refresh(new_file)
            return new_file
        except Exception as e:
            db.rollback()
            os.remove(file_path)  # Clean up if database save fails
            logger.error(f"Failed to save file to database: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to save file to the database.")

    @staticmethod
    async def delete_file(file_id: str, db: Session):
        file_to_delete = db.query(File).filter(File.Id == file_id).first()
        if not file_to_delete:
            raise HTTPException(status_code=404, detail="File not found")
    
        try:
            if os.path.exists(file_to_delete.FilePath):
                os.remove(file_to_delete.FilePath)
        except Exception as e:
            logger.error(f"Failed to delete file from filesystem: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to delete file from filesystem.")
    
        try:
            db.delete(file_to_delete)
            db.commit()
            return {"message": "File deleted successfully"}
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to delete file record from database: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to delete file record from database.")
