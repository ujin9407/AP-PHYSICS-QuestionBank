from fastapi import APIRouter, HTTPException, BackgroundTasks
from ..models import ConvertRequest, ConvertResponse, ConversionStatus
from ..services import DaTikZService, RenderService
from ..config import settings
import os
import logging
import asyncio

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/convert", tags=["convert"])

# In-memory storage for conversion results (use database in production)
conversion_results = {}


@router.post("", response_model=ConvertResponse)
async def convert_diagram(request: ConvertRequest, background_tasks: BackgroundTasks):
    """
    Convert handwritten diagram to TikZ code
    
    Args:
        request: Conversion request with image ID and options
        
    Returns:
        Conversion response with TikZ code and preview
    """
    try:
        # Find uploaded file
        image_path = None
        for filename in os.listdir(settings.upload_dir):
            if filename.startswith(request.image_id):
                image_path = os.path.join(settings.upload_dir, filename)
                break
        
        if not image_path or not os.path.exists(image_path):
            raise HTTPException(status_code=404, detail="Image not found")
        
        # Initialize conversion
        conversion_id = request.image_id
        conversion_results[conversion_id] = {
            "status": ConversionStatus.PROCESSING,
            "tikz_code": None,
            "preview_url": None,
            "error_message": None
        }
        
        # Process conversion in background
        background_tasks.add_task(
            process_conversion,
            conversion_id,
            image_path,
            request.diagram_type,
            request.description,
            request.use_template
        )
        
        return ConvertResponse(
            id=conversion_id,
            status=ConversionStatus.PROCESSING,
            tikz_code=None,
            preview_url=None
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error starting conversion: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")


@router.get("/{conversion_id}", response_model=ConvertResponse)
async def get_conversion_status(conversion_id: str):
    """
    Get the status of a conversion
    
    Args:
        conversion_id: ID of the conversion
        
    Returns:
        Current conversion status and results
    """
    if conversion_id not in conversion_results:
        raise HTTPException(status_code=404, detail="Conversion not found")
    
    result = conversion_results[conversion_id]
    
    return ConvertResponse(
        id=conversion_id,
        status=result["status"],
        tikz_code=result["tikz_code"],
        preview_url=result["preview_url"],
        error_message=result["error_message"]
    )


async def process_conversion(
    conversion_id: str,
    image_path: str,
    diagram_type: str,
    description: str = None,
    use_template: str = None
):
    """
    Background task to process diagram conversion
    """
    try:
        datikz_service = DaTikZService()
        render_service = RenderService()
        
        # Convert image to TikZ
        result = await datikz_service.convert_image_to_tikz(
            image_path=image_path,
            description=description,
            diagram_type=diagram_type
        )
        
        if not result["success"]:
            conversion_results[conversion_id].update({
                "status": ConversionStatus.FAILED,
                "error_message": result.get("error", "Conversion failed")
            })
            return
        
        tikz_code = result["tikz_code"]
        
        # Render preview
        render_result = await render_service.render_tikz(tikz_code, format="png")
        
        if render_result["success"]:
            preview_url = f"/api/outputs/{os.path.basename(render_result['output_path'])}"
        else:
            preview_url = None
        
        # Update results
        conversion_results[conversion_id].update({
            "status": ConversionStatus.COMPLETED,
            "tikz_code": tikz_code,
            "preview_url": preview_url
        })
        
        logger.info(f"Conversion completed successfully: {conversion_id}")
        
    except Exception as e:
        logger.error(f"Error in background conversion: {str(e)}")
        conversion_results[conversion_id].update({
            "status": ConversionStatus.FAILED,
            "error_message": str(e)
        })
