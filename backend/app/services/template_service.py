import os
import json
from typing import List, Optional
from ..models import Template, DiagramType
from ..config import settings
import logging

logger = logging.getLogger(__name__)


class TemplateService:
    """Service for managing physics diagram templates"""
    
    def __init__(self):
        self.template_dir = settings.template_dir
        self._ensure_templates_exist()
    
    def _ensure_templates_exist(self):
        """Create default templates if they don't exist"""
        templates_file = os.path.join(self.template_dir, "templates.json")
        
        if not os.path.exists(templates_file):
            default_templates = self._get_default_templates()
            with open(templates_file, "w") as f:
                json.dump(default_templates, f, indent=2)
    
    def _get_default_templates(self) -> List[dict]:
        """Get default physics diagram templates"""
        return [
            {
                "id": "mechanics_incline",
                "name": "Mass on Inclined Plane",
                "description": "A mass on an inclined plane with force vectors",
                "diagram_type": "mechanics",
                "tikz_code": """\\begin{tikzpicture}[scale=1.5]
    % Inclined plane
    \\draw[thick] (0,0) -- (4,2) -- (4,0) -- cycle;
    \\draw[fill=blue!20] (2,1) rectangle (2.5,1.5);
    \\node at (2.25,1.25) {$m$};
    
    % Normal force
    \\draw[->,red,thick] (2.25,1.5) -- (2.25,2.5) node[above] {$\\vec{N}$};
    % Weight
    \\draw[->,red,thick] (2.25,1.25) -- (2.25,0.25) node[below] {$\\vec{F_g}$};
    % Acceleration
    \\draw[->,green,thick] (2.5,1.25) -- (3.5,1.25) node[right] {$\\vec{a}$};
    
    % Angle
    \\draw (0.5,0) arc (0:26.57:0.5);
    \\node at (0.8,0.15) {$\\theta$};
\\end{tikzpicture}"""
            },
            {
                "id": "mechanics_pendulum",
                "name": "Simple Pendulum",
                "description": "A simple pendulum with angular displacement",
                "diagram_type": "mechanics",
                "tikz_code": """\\begin{tikzpicture}[scale=1.5]
    % Pivot point
    \\draw[fill] (0,3) circle (2pt);
    \\draw (0,3) -- (0,3.3) node[above] {Pivot};
    
    % String
    \\draw[thick] (0,3) -- (1.5,1);
    
    % Mass
    \\draw[fill=blue!30] (1.5,1) circle (0.3);
    \\node at (1.5,1) {$m$};
    
    % Angle arc
    \\draw[dashed] (0,3) -- (0,0.7);
    \\draw (0,2.3) arc (-90:-56.3:0.7);
    \\node at (0.3,2.1) {$\\theta$};
    
    % Forces
    \\draw[->,red,thick] (1.5,1) -- (1.5,-0.2) node[below] {$mg$};
    \\draw[->,blue,thick] (1.5,1) -- (0.3,2.2) node[above left] {$T$};
\\end{tikzpicture}"""
            },
            {
                "id": "electricity_circuit",
                "name": "Series Circuit",
                "description": "A basic series circuit with resistors",
                "diagram_type": "electricity",
                "tikz_code": """\\begin{tikzpicture}[scale=1.5]
    \\draw (0,0) to[battery1, l=$V$] (0,2)
          to[R, l=$R_1$] (2,2)
          to[R, l=$R_2$] (4,2)
          to[lamp, l=$L$] (4,0)
          to[short] (0,0);
    
    \\draw[->,blue,thick] (1,2.3) -- (2,2.3) node[midway,above] {$I$};
\\end{tikzpicture}"""
            },
            {
                "id": "electricity_parallel",
                "name": "Parallel Circuit",
                "description": "Resistors in parallel configuration",
                "diagram_type": "electricity",
                "tikz_code": """\\begin{tikzpicture}[scale=1.5]
    \\draw (0,0) to[battery1, l=$V$] (0,3)
          to[short] (1,3);
    \\draw (1,3) to[R, l=$R_1$] (3,3) to[short] (4,3);
    \\draw (1,3) to[short] (1,1.5) to[R, l=$R_2$] (3,1.5) to[short] (3,3);
    \\draw (4,3) to[short] (4,0) to[short] (0,0);
    
    \\draw[->,blue,thick] (0.3,3.3) -- (1.3,3.3) node[midway,above] {$I$};
\\end{tikzpicture}"""
            },
            {
                "id": "optics_lens",
                "name": "Converging Lens",
                "description": "Light rays through a converging lens",
                "diagram_type": "optics",
                "tikz_code": """\\begin{tikzpicture}[scale=1.5]
    % Lens
    \\draw[thick] (0,-1.5) to[out=20,in=-20] (0,1.5);
    \\draw[thick] (0.1,-1.5) to[out=20,in=-20] (0.1,1.5);
    
    % Optical axis
    \\draw[dashed] (-3,0) -- (4,0);
    
    % Light rays
    \\draw[->,blue,thick] (-3,1) -- (0,1);
    \\draw[->,blue,thick] (0,1) -- (3,-0.5);
    \\draw[->,blue,thick] (-3,0.5) -- (0,0.5);
    \\draw[->,blue,thick] (0,0.5) -- (3,-0.25);
    
    % Focal points
    \\node at (1.5,-0.3) {$F$};
    \\draw[fill] (1.5,0) circle (1pt);
    \\node at (-1.5,0.3) {$F'$};
    \\draw[fill] (-1.5,0) circle (1pt);
\\end{tikzpicture}"""
            },
            {
                "id": "thermodynamics_pv",
                "name": "PV Diagram",
                "description": "Pressure-Volume diagram for thermodynamic cycle",
                "diagram_type": "thermodynamics",
                "tikz_code": """\\begin{tikzpicture}[scale=1.5]
    % Axes
    \\draw[->,thick] (0,0) -- (4,0) node[right] {$V$};
    \\draw[->,thick] (0,0) -- (0,3) node[above] {$P$};
    
    % Cycle
    \\draw[blue,thick,->] (0.5,2.5) -- (3,2.5) node[midway,above] {1};
    \\draw[blue,thick,->] (3,2.5) -- (3,0.5) node[midway,right] {2};
    \\draw[blue,thick,->] (3,0.5) -- (0.5,0.5) node[midway,below] {3};
    \\draw[blue,thick,->] (0.5,0.5) -- (0.5,2.5) node[midway,left] {4};
    
    % State points
    \\node at (0.5,2.7) {$A$};
    \\node at (3.2,2.7) {$B$};
    \\node at (3.2,0.3) {$C$};
    \\node at (0.5,0.3) {$D$};
\\end{tikzpicture}"""
            },
            {
                "id": "quantum_energy",
                "name": "Energy Level Diagram",
                "description": "Quantum energy levels with transitions",
                "diagram_type": "quantum",
                "tikz_code": """\\begin{tikzpicture}[scale=1.5]
    % Energy levels
    \\draw[thick] (0,0) -- (3,0) node[right] {$E_1$};
    \\draw[thick] (0,1.5) -- (3,1.5) node[right] {$E_2$};
    \\draw[thick] (0,2.5) -- (3,2.5) node[right] {$E_3$};
    \\draw[thick] (0,3.2) -- (3,3.2) node[right] {$E_4$};
    
    % Transitions
    \\draw[->,red,thick] (1.5,2.5) -- (1.5,1.5) node[midway,right] {$h\\nu$};
    \\draw[->,blue,thick] (2,1.5) -- (2,0) node[midway,right] {$h\\nu'$};
    
    % Axis
    \\draw[->,thick] (-0.5,0) -- (-0.5,3.5) node[above] {$E$};
\\end{tikzpicture}"""
            }
        ]
    
    async def get_all_templates(self) -> List[Template]:
        """Get all available templates"""
        try:
            templates_file = os.path.join(self.template_dir, "templates.json")
            
            with open(templates_file, "r") as f:
                templates_data = json.load(f)
            
            templates = [Template(**template) for template in templates_data]
            return templates
            
        except Exception as e:
            logger.error(f"Error loading templates: {str(e)}")
            return []
    
    async def get_template_by_id(self, template_id: str) -> Optional[Template]:
        """Get a specific template by ID"""
        templates = await self.get_all_templates()
        for template in templates:
            if template.id == template_id:
                return template
        return None
    
    async def get_templates_by_type(self, diagram_type: DiagramType) -> List[Template]:
        """Get templates filtered by diagram type"""
        all_templates = await self.get_all_templates()
        return [t for t in all_templates if t.diagram_type == diagram_type]
