from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class DiagramType(str, Enum):
    MECHANICS = "mechanics"
    ELECTRICITY = "electricity"
    OPTICS = "optics"
    THERMODYNAMICS = "thermodynamics"
    QUANTUM = "quantum"
    GENERAL = "general"


class ConversionStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class UploadResponse(BaseModel):
    id: str
    filename: str
    upload_time: datetime
    status: str
    message: str


class ConvertRequest(BaseModel):
    image_id: str
    diagram_type: DiagramType = DiagramType.GENERAL
    description: Optional[str] = None
    use_template: Optional[str] = None


class ConvertResponse(BaseModel):
    id: str
    status: ConversionStatus
    tikz_code: Optional[str] = None
    preview_url: Optional[str] = None
    error_message: Optional[str] = None


class Template(BaseModel):
    id: str
    name: str
    description: str
    diagram_type: DiagramType
    tikz_code: str
    preview_image: Optional[str] = None


class TemplateListResponse(BaseModel):
    templates: List[Template]


class RenderRequest(BaseModel):
    tikz_code: str
    format: str = Field(default="png", pattern="^(png|pdf|svg)$")


class RenderResponse(BaseModel):
    id: str
    format: str
    output_url: str


class PDFExportRequest(BaseModel):
    diagram_id: str
    include_code: bool = False
    title: Optional[str] = None


class PDFExportResponse(BaseModel):
    pdf_url: str
    filename: str
