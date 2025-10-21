from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from ..models import PDFExportRequest, PDFExportResponse
from ..services import PDFService, RenderService
from ..config import settings
from ..routers.convert import conversion_results
import os
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/export", tags=["export"])


@router.post("/pdf", response_model=PDFExportResponse)
async def export_to_pdf(request: PDFExportRequest):
    """
    Export diagram to PDF
    
    Args:
        request: PDF export request with diagram ID and options
        
    Returns:
        PDF export response with download URL
    """
    try:
        # Get conversion result
        if request.diagram_id not in conversion_results:
            raise HTTPException(status_code=404, detail="Diagram not found")
        
        result = conversion_results[request.diagram_id]
        
        if result["status"] != "completed":
            raise HTTPException(
                status_code=400,
                detail="Diagram conversion not completed"
            )
        
        # Get preview image path
        if result["preview_url"]:
            preview_filename = result["preview_url"].split("/")[-1]
            image_path = os.path.join(settings.output_dir, preview_filename)
        else:
            raise HTTPException(status_code=404, detail="Preview image not found")
        
        # Create PDF
        pdf_service = PDFService()
        
        pdf_result = await pdf_service.create_diagram_pdf(
            diagram_image_path=image_path,
            tikz_code=result["tikz_code"] if request.include_code else None,
            title=request.title,
            include_code=request.include_code
        )
        
        if not pdf_result["success"]:
            raise HTTPException(
                status_code=500,
                detail=pdf_result.get("error", "PDF creation failed")
            )
        
        pdf_url = f"/api/export/download/{pdf_result['filename']}"
        
        return PDFExportResponse(
            pdf_url=pdf_url,
            filename=pdf_result["filename"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error exporting to PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=f"PDF export failed: {str(e)}")


@router.get("/download/{filename}")
async def download_pdf(filename: str):
    """
    Download exported PDF file
    
    Args:
        filename: Name of the PDF file
        
    Returns:
        PDF file for download
    """
    try:
        file_path = os.path.join(settings.output_dir, filename)
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        
        return FileResponse(
            file_path,
            media_type="application/pdf",
            filename=filename
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")


@router.get("/outputs/{filename}")
async def get_output_file(filename: str):
    """
    Get rendered output file (images)
    
    Args:
        filename: Name of the output file
        
    Returns:
        Output file
    """
    try:
        file_path = os.path.join(settings.output_dir, filename)
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        
        return FileResponse(file_path)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving output file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving file: {str(e)}")
