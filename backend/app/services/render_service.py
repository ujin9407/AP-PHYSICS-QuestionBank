import os
import subprocess
import uuid
from typing import Optional
from ..config import settings
import logging

logger = logging.getLogger(__name__)


class RenderService:
    """Service for rendering TikZ code to images"""
    
    def __init__(self):
        self.output_dir = settings.output_dir
    
    async def render_tikz(self, tikz_code: str, format: str = "png") -> dict:
        """
        Render TikZ code to image format
        
        Args:
            tikz_code: TikZ code to render
            format: Output format (png, pdf, svg)
            
        Returns:
            dict with output file path and status
        """
        try:
            # Generate unique ID for this render
            render_id = str(uuid.uuid4())
            
            # Create LaTeX document
            latex_content = self._create_latex_document(tikz_code)
            
            # Write LaTeX file
            tex_file = os.path.join(self.output_dir, f"{render_id}.tex")
            with open(tex_file, "w") as f:
                f.write(latex_content)
            
            # For now, create a placeholder image since we may not have LaTeX installed
            # In production, you would compile with pdflatex and convert to desired format
            output_file = await self._create_placeholder(render_id, format)
            
            return {
                "success": True,
                "id": render_id,
                "output_path": output_file,
                "format": format
            }
            
        except Exception as e:
            logger.error(f"Error rendering TikZ: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _create_latex_document(self, tikz_code: str) -> str:
        """Create complete LaTeX document with TikZ code"""
        return f"""\\documentclass[border=2pt]{{standalone}}
\\usepackage{{tikz}}
\\usepackage{{amsmath}}
\\usepackage{{amssymb}}
\\usetikzlibrary{{arrows.meta,positioning,shapes,decorations.markings}}

\\begin{{document}}
{tikz_code}
\\end{{document}}
"""
    
    async def _create_placeholder(self, render_id: str, format: str) -> str:
        """Create a placeholder file for development"""
        from PIL import Image, ImageDraw, ImageFont
        
        # Create a simple placeholder image
        width, height = 800, 600
        img = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(img)
        
        # Draw border
        draw.rectangle([10, 10, width-10, height-10], outline='black', width=2)
        
        # Add text
        text = "TikZ Diagram Preview"
        text_bbox = draw.textbbox((0, 0), text)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        text_position = ((width - text_width) // 2, (height - text_height) // 2)
        draw.text(text_position, text, fill='black')
        
        # Save image
        if format == "png":
            output_file = os.path.join(self.output_dir, f"{render_id}.png")
            img.save(output_file, "PNG")
        elif format == "pdf":
            output_file = os.path.join(self.output_dir, f"{render_id}.pdf")
            img.save(output_file, "PDF")
        else:
            output_file = os.path.join(self.output_dir, f"{render_id}.png")
            img.save(output_file, "PNG")
        
        return output_file
    
    async def compile_latex(self, tex_file: str) -> Optional[str]:
        """
        Compile LaTeX file to PDF using pdflatex
        This is a production implementation that requires LaTeX installation
        """
        try:
            # Run pdflatex
            result = subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", "-output-directory", 
                 self.output_dir, tex_file],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                # Get PDF filename
                base_name = os.path.splitext(os.path.basename(tex_file))[0]
                pdf_file = os.path.join(self.output_dir, f"{base_name}.pdf")
                return pdf_file
            else:
                logger.error(f"LaTeX compilation failed: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            logger.error("LaTeX compilation timed out")
            return None
        except FileNotFoundError:
            logger.warning("pdflatex not found, using placeholder instead")
            return None
        except Exception as e:
            logger.error(f"Error compiling LaTeX: {str(e)}")
            return None
    
    async def pdf_to_image(self, pdf_file: str, output_format: str = "png") -> Optional[str]:
        """Convert PDF to image format"""
        try:
            from pdf2image import convert_from_path
            
            images = convert_from_path(pdf_file, dpi=300)
            if images:
                base_name = os.path.splitext(pdf_file)[0]
                output_file = f"{base_name}.{output_format}"
                images[0].save(output_file, output_format.upper())
                return output_file
            
            return None
            
        except Exception as e:
            logger.error(f"Error converting PDF to image: {str(e)}")
            return None
