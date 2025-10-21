from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from ..models import RenderRequest, RenderResponse
from ..services import RenderService
import os
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/render", tags=["render"])


@router.post("", response_model=RenderResponse)
async def render_tikz(request: RenderRequest):
    """
    Render TikZ code to image
    
    Args:
        request: Render request with TikZ code and format
        
    Returns:
        Render response with output URL
    """
    try:
        render_service = RenderService()
        
        # Render the TikZ code
        result = await render_service.render_tikz(
            tikz_code=request.tikz_code,
            format=request.format
        )
        
        if not result["success"]:
            raise HTTPException(
                status_code=500,
                detail=result.get("error", "Rendering failed")
            )
        
        # Get output URL
        output_filename = os.path.basename(result["output_path"])
        output_url = f"/api/outputs/{output_filename}"
        
        return RenderResponse(
            id=result["id"],
            format=result["format"],
            output_url=output_url
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error rendering TikZ: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Rendering failed: {str(e)}")
