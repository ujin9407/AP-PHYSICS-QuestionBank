import httpx
import base64
from typing import Optional
from ..config import settings
import logging

logger = logging.getLogger(__name__)


class DaTikZService:
    """Service for interacting with DaTikZv2 API"""
    
    def __init__(self):
        self.api_url = settings.datikz_api_url
        self.api_key = settings.datikz_api_key
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def convert_image_to_tikz(
        self, 
        image_path: str, 
        description: Optional[str] = None,
        diagram_type: str = "general"
    ) -> dict:
        """
        Convert handwritten diagram image to TikZ code using DaTikZv2
        
        Args:
            image_path: Path to the image file
            description: Optional text description to guide conversion
            diagram_type: Type of physics diagram (mechanics, electricity, etc.)
            
        Returns:
            dict with 'tikz_code' and 'success' status
        """
        try:
            # Read and encode image
            with open(image_path, "rb") as image_file:
                image_data = base64.b64encode(image_file.read()).decode('utf-8')
            
            # Prepare prompt based on diagram type
            prompt = self._create_prompt(diagram_type, description)
            
            # For now, we'll use a mock implementation since we don't have actual API access
            # In production, this would call the real DaTikZv2 API
            tikz_code = await self._mock_conversion(image_path, prompt, diagram_type)
            
            return {
                "success": True,
                "tikz_code": tikz_code,
                "diagram_type": diagram_type
            }
            
        except Exception as e:
            logger.error(f"Error converting image to TikZ: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _create_prompt(self, diagram_type: str, description: Optional[str] = None) -> str:
        """Create appropriate prompt for DaTikZv2 based on diagram type"""
        
        base_prompts = {
            "mechanics": "Convert this handwritten physics diagram to TikZ code. Focus on forces, vectors, motion, and mechanical systems.",
            "electricity": "Convert this handwritten electrical circuit or field diagram to TikZ code. Include proper circuit symbols and field lines.",
            "optics": "Convert this handwritten optics diagram to TikZ code. Include light rays, lenses, mirrors, and optical components.",
            "thermodynamics": "Convert this handwritten thermodynamics diagram to TikZ code. Include heat flow, PV diagrams, and thermodynamic systems.",
            "quantum": "Convert this handwritten quantum mechanics diagram to TikZ code. Include wave functions, energy levels, and quantum states.",
            "general": "Convert this handwritten physics diagram to clean TikZ code."
        }
        
        prompt = base_prompts.get(diagram_type, base_prompts["general"])
        
        if description:
            prompt += f" Additional context: {description}"
        
        return prompt
    
    async def _mock_conversion(self, image_path: str, prompt: str, diagram_type: str) -> str:
        """
        Mock conversion for development/testing
        Replace this with actual API call in production
        """
        
        # Return appropriate template based on diagram type
        templates = {
            "mechanics": """\\begin{tikzpicture}[scale=1.5]
    % Mass on incline
    \\draw[thick] (0,0) -- (4,2) -- (4,0) -- cycle;
    \\draw[fill=blue!20] (2,1) rectangle (2.5,1.5);
    \\node at (2.25,1.25) {$m$};
    
    % Forces
    \\draw[->,red,thick] (2.25,1.5) -- (2.25,2.5) node[above] {$\\vec{N}$};
    \\draw[->,red,thick] (2.25,1.25) -- (2.25,0.25) node[below] {$\\vec{F_g}$};
    \\draw[->,green,thick] (2.5,1.25) -- (3.5,1.25) node[right] {$\\vec{a}$};
    
    % Angle
    \\draw (0.5,0) arc (0:26.57:0.5);
    \\node at (0.8,0.15) {$\\theta$};
\\end{tikzpicture}""",
            
            "electricity": """\\begin{tikzpicture}[scale=1.5]
    % Circuit components
    \\draw (0,0) to[battery1, l=$V$] (0,2)
          to[R, l=$R_1$] (2,2)
          to[R, l=$R_2$] (4,2)
          to[lamp, l=$L$] (4,0)
          to[short] (0,0);
    
    % Current direction
    \\draw[->,blue,thick] (1,2.3) -- (2,2.3) node[midway,above] {$I$};
\\end{tikzpicture}""",
            
            "optics": """\\begin{tikzpicture}[scale=1.5]
    % Lens
    \\draw[thick] (0,-1.5) to[out=20,in=-20] (0,1.5);
    \\draw[thick] (0.1,-1.5) to[out=20,in=-20] (0.1,1.5);
    
    % Optical axis
    \\draw[dashed] (-2,0) -- (4,0);
    
    % Light rays
    \\draw[->,blue,thick] (-2,1) -- (0,1);
    \\draw[->,blue,thick] (0,1) -- (3,-0.5);
    \\draw[->,blue,thick] (-2,0.5) -- (0,0.5);
    \\draw[->,blue,thick] (0,0.5) -- (3,-0.3);
    
    % Focal points
    \\node at (1.5,-0.3) {$F$};
    \\draw[fill] (1.5,0) circle (1pt);
\\end{tikzpicture}""",
            
            "general": """\\begin{tikzpicture}[scale=1.5]
    % Generic physics diagram
    \\draw[thick,->] (0,0) -- (3,0) node[right] {$x$};
    \\draw[thick,->] (0,0) -- (0,3) node[above] {$y$};
    
    % Vector
    \\draw[->,red,very thick] (0,0) -- (2,2) node[midway,above left] {$\\vec{F}$};
    
    % Point
    \\draw[fill] (1,1) circle (2pt) node[below right] {$P$};
\\end{tikzpicture}"""
        }
        
        return templates.get(diagram_type, templates["general"])
    
    async def validate_tikz_code(self, tikz_code: str) -> bool:
        """Validate TikZ code syntax"""
        # Basic validation - check for required tikzpicture environment
        return "\\begin{tikzpicture}" in tikz_code and "\\end{tikzpicture}" in tikz_code
