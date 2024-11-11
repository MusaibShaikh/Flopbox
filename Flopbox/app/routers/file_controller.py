from fastapi import APIRouter, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from loguru import logger
import os
from handlers.file_service import FileService
from models.db_context import DbObject
from models.models import File  
from typing import List 
from models.file import FileResp

router = APIRouter()
db_context = DbObject()
db_context.CreateConnection("mysql+pymysql://root:ororZZKkPTnvAPsrdXHDKuUjEsfSSOiQ@junction.proxy.rlwy.net:28681/railway")
_current_db_session = db_context.GetCurrentSession()

# Ensure the upload directory exists
UPLOAD_DIRECTORY = "uploads"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

@router.post("/file/")
async def upload_file(
    file: UploadFile,
    user_id: str = Form(...),
    comment: str = Form(None),
):
    try:
        # Read the file content and save to the database and filesystem
        file_content = await file.read()
        new_file = await FileService.upload_file(file_content, file.filename, user_id, comment, _current_db_session)
        return {
            "filename": new_file.Filename,
            "md5_hash": new_file.MD5Hash,
            "message": "File uploaded successfully."
        }
    except Exception as e:
        logger.error(f"Upload file failed: {str(e)}")
        raise HTTPException(status_code=500, detail="File upload failed")

@router.get("/file/{file_id}/")
async def download_file(file_id: str):
    # Retrieve the file from the database
    try:
        file_record = _current_db_session.query(File).filter(File.Id == file_id).first()
        if not file_record:
            raise HTTPException(status_code=404, detail="File not found")
        
        # Return the file as a response
        return FileResponse(path=file_record.FilePath, filename=file_record.Filename)
    except Exception as e:
        logger.error(f"Download file failed: {str(e)}")
        raise HTTPException(status_code=500, detail="File download failed")

@router.delete("/file/{file_id}/")
async def delete_file(file_id: str):
    # Call the service function to delete the file
    try:
        result = await FileService.delete_file(file_id, _current_db_session)
        return result
    except Exception as e:
        logger.error(f"Delete file failed: {str(e)}")
        raise HTTPException(status_code=500, detail="File deletion failed")

@router.get("/files/user/{user_id}", response_model=List[FileResp])
async def get_files_for_user(user_id: str):
    try:
        files = _current_db_session.query(File).filter(File.UserId == user_id).all()
        if not files:
            raise HTTPException(status_code=404, detail="No files found for this user")
        return files
    except Exception as e:
        logger.error(f"Error retrieving files for user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve files")