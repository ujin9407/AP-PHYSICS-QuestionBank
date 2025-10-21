import os
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Preformatted
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
from typing import Optional
from ..config import settings
import logging

logger = logging.getLogger(__name__)


class PDFService:
    """Service for generating PDF exports"""
    
    def __init__(self):
        self.output_dir = settings.output_dir
    
    async def create_diagram_pdf(
        self, 
        diagram_image_path: str,
        tikz_code: Optional[str] = None,
        title: Optional[str] = None,
        include_code: bool = False
    ) -> dict:
        """
        Create a PDF document with the diagram and optionally the TikZ code
        
        Args:
            diagram_image_path: Path to the rendered diagram image
            tikz_code: TikZ source code
            title: Title for the document
            include_code: Whether to include the TikZ source code
            
        Returns:
            dict with PDF file path and status
        """
        try:
            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            pdf_filename = f"diagram_{timestamp}.pdf"
            pdf_path = os.path.join(self.output_dir, pdf_filename)
            
            # Create PDF document
            doc = SimpleDocTemplate(
                pdf_path,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18
            )
            
            # Container for PDF elements
            story = []
            
            # Get styles
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor='#2C3E50',
                spaceAfter=30,
                alignment=TA_CENTER
            )
            
            # Add title
            if title:
                story.append(Paragraph(title, title_style))
            else:
                story.append(Paragraph("Physics Diagram", title_style))
            
            story.append(Spacer(1, 0.2*inch))
            
            # Add timestamp
            date_style = ParagraphStyle(
                'DateStyle',
                parent=styles['Normal'],
                fontSize=10,
                textColor='#7F8C8D',
                alignment=TA_CENTER
            )
            story.append(Paragraph(f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", date_style))
            story.append(Spacer(1, 0.5*inch))
            
            # Add diagram image
            if os.path.exists(diagram_image_path):
                img = RLImage(diagram_image_path)
                # Scale image to fit page width
                img_width, img_height = img.imageWidth, img.imageHeight
                aspect = img_height / float(img_width)
                
                # Maximum width (page width minus margins)
                max_width = 6.5 * inch
                img.drawWidth = min(img_width, max_width)
                img.drawHeight = img.drawWidth * aspect
                
                story.append(img)
                story.append(Spacer(1, 0.5*inch))
            
            # Add TikZ code if requested
            if include_code and tikz_code:
                story.append(Paragraph("TikZ Source Code:", styles['Heading2']))
                story.append(Spacer(1, 0.2*inch))
                
                # Format code
                code_style = ParagraphStyle(
                    'CodeStyle',
                    parent=styles['Code'],
                    fontSize=8,
                    leftIndent=20,
                    rightIndent=20,
                    textColor='#2C3E50',
                    backColor='#ECF0F1'
                )
                
                code_paragraph = Preformatted(tikz_code, code_style)
                story.append(code_paragraph)
            
            # Build PDF
            doc.build(story)
            
            return {
                "success": True,
                "pdf_path": pdf_path,
                "filename": pdf_filename
            }
            
        except Exception as e:
            logger.error(f"Error creating PDF: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def create_quick_pdf(self, image_path: str) -> Optional[str]:
        """
        Create a simple PDF from an image
        Faster method for quick exports
        """
        try:
            from PIL import Image
            
            # Load image
            img = Image.open(image_path)
            
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Generate PDF filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            pdf_filename = f"quick_export_{timestamp}.pdf"
            pdf_path = os.path.join(self.output_dir, pdf_filename)
            
            # Save as PDF
            img.save(pdf_path, "PDF", resolution=100.0)
            
            return pdf_path
            
        except Exception as e:
            logger.error(f"Error creating quick PDF: {str(e)}")
            return None
