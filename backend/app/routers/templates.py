from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from ..models import Template, TemplateListResponse, DiagramType
from ..services import TemplateService
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/templates", tags=["templates"])


@router.get("", response_model=TemplateListResponse)
async def get_templates(
    diagram_type: Optional[DiagramType] = Query(None, description="Filter by diagram type")
):
    """
    Get all available physics diagram templates
    
    Args:
        diagram_type: Optional filter by diagram type
        
    Returns:
        List of available templates
    """
    try:
        template_service = TemplateService()
        
        if diagram_type:
            templates = await template_service.get_templates_by_type(diagram_type)
        else:
            templates = await template_service.get_all_templates()
        
        return TemplateListResponse(templates=templates)
        
    except Exception as e:
        logger.error(f"Error retrieving templates: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving templates: {str(e)}")


@router.get("/{template_id}", response_model=Template)
async def get_template(template_id: str):
    """
    Get a specific template by ID
    
    Args:
        template_id: ID of the template
        
    Returns:
        Template details
    """
    try:
        template_service = TemplateService()
        template = await template_service.get_template_by_id(template_id)
        
        if not template:
            raise HTTPException(status_code=404, detail="Template not found")
        
        return template
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving template: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving template: {str(e)}")
