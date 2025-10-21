from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import os
import uuid
from datetime import datetime
import aiofiles
from ..models import UploadResponse
from ..config import settings
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/upload", tags=["upload"])


@router.post("", response_model=UploadResponse)
async def upload_diagram(file: UploadFile = File(...)):
    """
    Upload a handwritten physics diagram image
    
    Args:
        file: Image file (PNG, JPG, JPEG)
        
    Returns:
        Upload response with file ID and status
    """
    try:
        # Validate file type
        allowed_types = ["image/png", "image/jpeg", "image/jpg"]
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed types: {', '.join(allowed_types)}"
            )
        
        # Check file size
        contents = await file.read()
        file_size = len(contents)
        
        if file_size > settings.max_upload_size:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size: {settings.max_upload_size / 1024 / 1024}MB"
            )
        
        # Generate unique ID and filename
        file_id = str(uuid.uuid4())
        file_extension = os.path.splitext(file.filename)[1]
        new_filename = f"{file_id}{file_extension}"
        file_path = os.path.join(settings.upload_dir, new_filename)
        
        # Save file
        async with aiofiles.open(file_path, "wb") as f:
            await f.write(contents)
        
        logger.info(f"File uploaded successfully: {new_filename}")
        
        return UploadResponse(
            id=file_id,
            filename=new_filename,
            upload_time=datetime.now(),
            status="success",
            message="File uploaded successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.get("/{file_id}")
async def get_uploaded_file(file_id: str):
    """
    Retrieve an uploaded file
    
    Args:
        file_id: ID of the uploaded file
        
    Returns:
        The uploaded image file
    """
    try:
        # Find file with this ID
        for filename in os.listdir(settings.upload_dir):
            if filename.startswith(file_id):
                file_path = os.path.join(settings.upload_dir, filename)
                return FileResponse(file_path)
        
        raise HTTPException(status_code=404, detail="File not found")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving file: {str(e)}")
