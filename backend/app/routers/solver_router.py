"""
API Router for AI Physics Problem Solver
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict
import uuid
import shutil
from pathlib import Path
import logging

from ..services.ai_solver import OCRService, PhysicsProblemSolver
from ..config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/solver", tags=["solver"])

# Initialize services
ocr_service = OCRService()
problem_solver = PhysicsProblemSolver()


class SolveRequest(BaseModel):
    """Request model for solving a problem"""
    problem_text: Optional[str] = None
    image_id: Optional[str] = None


class SolveResponse(BaseModel):
    """Response model for solved problem"""
    success: bool
    solution_id: str
    problem_text: Optional[str] = None
    solution: Optional[Dict] = None
    error: Optional[str] = None


@router.post("/upload-problem", response_model=Dict)
async def upload_problem_image(file: UploadFile = File(...)):
    """
    Upload a handwritten physics problem image
    
    Args:
        file: Image file containing handwritten physics problem
        
    Returns:
        Upload information with image_id for later use
    """
    try:
        # Generate unique ID
        image_id = str(uuid.uuid4())
        
        # Save uploaded file
        file_extension = Path(file.filename).suffix
        file_path = Path(settings.upload_dir) / f"{image_id}{file_extension}"
        
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        logger.info(f"Problem image uploaded: {file_path}")
        
        # Extract text using OCR
        ocr_result = await ocr_service.extract_text_from_image(str(file_path))
        
        return {
            "success": True,
            "image_id": image_id,
            "filename": file.filename,
            "file_path": str(file_path),
            "ocr_text": ocr_result.get("text") if ocr_result["success"] else None,
            "ocr_confidence": ocr_result.get("confidence")
        }
        
    except Exception as e:
        logger.error(f"Upload failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/solve", response_model=SolveResponse)
async def solve_problem(request: SolveRequest):
    """
    Solve a physics problem using AI
    
    Args:
        request: Problem text or image_id
        
    Returns:
        Complete solution with step-by-step explanation
    """
    try:
        solution_id = str(uuid.uuid4())
        
        # Get problem text
        problem_text = request.problem_text
        image_base64 = None
        
        if request.image_id and not problem_text:
            # Load image and extract text
            image_path = Path(settings.upload_dir) / f"{request.image_id}.png"
            if not image_path.exists():
                # Try other extensions
                for ext in ['.jpg', '.jpeg', '.png']:
                    test_path = Path(settings.upload_dir) / f"{request.image_id}{ext}"
                    if test_path.exists():
                        image_path = test_path
                        break
            
            if image_path.exists():
                ocr_result = await ocr_service.extract_text_from_image(str(image_path))
                problem_text = ocr_result.get("text")
                image_base64 = ocr_result.get("image_base64")
            else:
                raise HTTPException(status_code=404, detail="Image not found")
        
        if not problem_text:
            raise HTTPException(status_code=400, detail="No problem text provided")
        
        # Solve the problem (with image if available)
        result = await problem_solver.solve_problem(
            problem_text, 
            image_base64,
            str(image_path) if image_path.exists() else None
        )
        
        if not result["success"]:
            return SolveResponse(
                success=False,
                solution_id=solution_id,
                error=result.get("error")
            )
        
        return SolveResponse(
            success=True,
            solution_id=solution_id,
            problem_text=problem_text,
            solution=result["solution"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Problem solving failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/solution/{solution_id}")
async def get_solution(solution_id: str):
    """
    Get a previously generated solution
    
    Args:
        solution_id: ID of the solution
        
    Returns:
        Solution data
    """
    # In production, retrieve from database
    # For now, return a mock response
    return {
        "success": True,
        "solution_id": solution_id,
        "message": "Solution retrieval not yet implemented"
    }
