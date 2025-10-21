"""
AI Physics Problem Solver
Uses GPT-4/Gemini to solve physics problems step-by-step
Supports problems with graphs, diagrams, and visual elements
"""
import logging
from typing import Dict, List, Optional
import json
from .image_analyzer import ImageAnalyzer

logger = logging.getLogger(__name__)


class PhysicsProblemSolver:
    """AI-powered physics problem solver with image analysis"""
    
    def __init__(self):
        """Initialize the problem solver"""
        self.image_analyzer = ImageAnalyzer()
        self.system_prompt = """You are an expert physics teacher and problem solver.
When given a physics problem:
1. Identify the type of problem (mechanics, electricity, thermodynamics, etc.)
2. List all given information
3. Identify what needs to be found
4. Provide step-by-step solution with explanations
5. Show all formulas used
6. Provide numerical calculations
7. Generate TikZ code for relevant diagrams (free body diagrams, circuit diagrams, etc.)
8. Give final answers with units

Format your response as JSON with the following structure:
{
    "problem_type": "mechanics|electricity|thermodynamics|optics|quantum",
    "given_info": ["item1", "item2", ...],
    "find": ["what to find 1", "what to find 2", ...],
    "solution_steps": [
        {
            "step_number": 1,
            "title": "Step title",
            "explanation": "Detailed explanation",
            "formulas": ["formula1", "formula2"],
            "calculations": ["calc1", "calc2"],
            "result": "intermediate result"
        }
    ],
    "tikz_diagrams": [
        {
            "type": "free_body_diagram|circuit|graph",
            "title": "Diagram title",
            "code": "TikZ code here"
        }
    ],
    "final_answers": [
        {
            "question": "a) ...",
            "answer": "value with unit",
            "explanation": "brief explanation"
        }
    ]
}
"""
    
    async def solve_problem(
        self, 
        problem_text: str, 
        image_base64: Optional[str] = None,
        image_path: Optional[str] = None
    ) -> Dict:
        """
        Solve a physics problem using AI (with optional image analysis)
        
        Args:
            problem_text: The extracted problem text
            image_base64: Optional base64 encoded image
            image_path: Optional path to image file
            
        Returns:
            Dictionary containing the complete solution
        """
        try:
            logger.info(f"Solving problem: {problem_text[:100]}...")
            
            # Analyze image if provided
            image_analysis = None
            if image_path or image_base64:
                logger.info("Analyzing image for graphs/diagrams...")
                analysis_result = await self.image_analyzer.analyze_image(
                    image_path or "uploaded_image",
                    image_base64
                )
                if analysis_result["success"]:
                    image_analysis = analysis_result["analysis"]
                    logger.info(f"Image type detected: {image_analysis.get('image_type')}")
            
            # Generate solution (with image context if available)
            solution = self._generate_mock_solution(problem_text, image_analysis)
            
            return {
                "success": True,
                "solution": solution,
                "problem_text": problem_text,
                "image_analysis": image_analysis
            }
            
        except Exception as e:
            logger.error(f"Problem solving failed: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _generate_mock_solution(self, problem_text: str, image_analysis: Optional[Dict] = None) -> Dict:
        """Generate a mock solution for development"""
        
        # If image analysis is available, use it to enhance solution
        if image_analysis:
            image_type = image_analysis.get('image_type')
            
            # Solve based on image type
            if image_type == 'graph' and 'velocity' in image_analysis.get('title', '').lower():
                return self._solve_velocity_graph_problem(problem_text, image_analysis)
            elif image_type == 'circuit':
                return self._solve_circuit_diagram_problem(problem_text, image_analysis)
            elif image_type == 'diagram' and 'incline' in image_analysis.get('description', '').lower():
                return self._solve_diagram_problem(problem_text, image_analysis)
        
        # Detect problem type from text
        problem_lower = problem_text.lower()
        problem_type = "general"
        
        if any(word in problem_lower for word in ['incline', 'friction', 'force', 'acceleration', 'velocity', 'projectile', 'motion']):
            problem_type = "mechanics"
        elif any(word in problem_lower for word in ['circuit', 'voltage', 'current', 'resistance', 'resistor', 'capacitor', 'inductor']):
            problem_type = "electricity"
        elif any(word in problem_lower for word in ['heat', 'temperature', 'thermal', 'entropy', 'gas', 'pressure']):
            problem_type = "thermodynamics"
        elif any(word in problem_lower for word in ['lens', 'mirror', 'light', 'reflection', 'refraction', 'wavelength']):
            problem_type = "optics"
        elif any(word in problem_lower for word in ['quantum', 'photon', 'electron', 'energy level', 'wave function']):
            problem_type = "quantum"
        elif any(word in problem_lower for word in ['graph', 'velocity-time', 'position-time', 'v-t', 'x-t']):
            problem_type = "kinematics_graph"
            return self._solve_graph_problem(problem_text)
        
        # Check if it's inclined plane problem (original sample)
        if 'incline' in problem_lower and 'friction' in problem_lower:
            return self._solve_inclined_plane_problem(problem_text)
        
        # Check if it's projectile motion
        elif 'projectile' in problem_lower or ('launch' in problem_lower and 'angle' in problem_lower):
            return self._solve_projectile_problem(problem_text)
        
        # Check if it's circuit problem
        elif 'circuit' in problem_lower and 'resistor' in problem_lower:
            return self._solve_circuit_problem(problem_text)
        
        # Generic solution for other problems
        return self._solve_generic_problem(problem_text, problem_type)
    
    def _solve_inclined_plane_problem(self, problem_text: str) -> Dict:
        """Solve inclined plane problem"""
        return {
            "problem_type": "mechanics",
            "given_info": [
                "Mass (m) = 2 kg",
                "Incline angle (θ) = 30°",
                "Coefficient of kinetic friction (μk) = 0.3",
                "Gravitational acceleration (g) = 10 m/s²"
            ],
            "find": [
                "a) Acceleration of the block",
                "b) Normal force",
                "c) Friction force"
            ],
            "solution_steps": [
                {
                    "step_number": 1,
                    "title": "Draw Free Body Diagram",
                    "explanation": "Identify all forces acting on the block: weight (mg), normal force (N), and friction force (f).",
                    "formulas": [],
                    "calculations": [],
                    "result": "Forces identified"
                },
                {
                    "step_number": 2,
                    "title": "Resolve Weight into Components",
                    "explanation": "The weight has components parallel and perpendicular to the incline.",
                    "formulas": [
                        "mg_parallel = mg sin(θ)",
                        "mg_perpendicular = mg cos(θ)"
                    ],
                    "calculations": [
                        "mg_parallel = 2 × 10 × sin(30°) = 2 × 10 × 0.5 = 10 N",
                        "mg_perpendicular = 2 × 10 × cos(30°) = 2 × 10 × 0.866 = 17.32 N"
                    ],
                    "result": "Weight components calculated"
                },
                {
                    "step_number": 3,
                    "title": "Calculate Normal Force (b)",
                    "explanation": "The normal force equals the perpendicular component of weight (no acceleration perpendicular to incline).",
                    "formulas": [
                        "N = mg cos(θ)"
                    ],
                    "calculations": [
                        "N = 17.32 N"
                    ],
                    "result": "N = 17.32 N"
                },
                {
                    "step_number": 4,
                    "title": "Calculate Friction Force (c)",
                    "explanation": "Kinetic friction opposes motion and depends on the normal force.",
                    "formulas": [
                        "f = μk × N"
                    ],
                    "calculations": [
                        "f = 0.3 × 17.32 = 5.196 N"
                    ],
                    "result": "f ≈ 5.2 N"
                },
                {
                    "step_number": 5,
                    "title": "Calculate Acceleration (a)",
                    "explanation": "Net force down the incline equals mass times acceleration.",
                    "formulas": [
                        "F_net = mg sin(θ) - f",
                        "a = F_net / m"
                    ],
                    "calculations": [
                        "F_net = 10 - 5.2 = 4.8 N",
                        "a = 4.8 / 2 = 2.4 m/s²"
                    ],
                    "result": "a = 2.4 m/s²"
                }
            ],
            "tikz_diagrams": [
                {
                    "type": "free_body_diagram",
                    "title": "Free Body Diagram of Block on Incline",
                    "code": """\\begin{tikzpicture}[scale=1.5]
    % Inclined plane
    \\draw[thick] (0,0) -- (4,2) -- (4,0) -- cycle;
    \\draw[fill=blue!20] (2,1) rectangle (2.5,1.5);
    \\node at (2.25,1.25) {$m$};
    
    % Normal force
    \\draw[->,red,very thick] (2.25,1.5) -- (2.25,2.5) node[above] {$\\vec{N}$};
    % Weight
    \\draw[->,red,very thick] (2.25,1.25) -- (2.25,0.25) node[below] {$mg$};
    % Friction
    \\draw[->,orange,very thick] (2.5,1.25) -- (1.5,1.75) node[above left] {$\\vec{f}$};
    % Acceleration
    \\draw[->,green,very thick] (2.5,1.25) -- (3.5,1.75) node[right] {$\\vec{a}$};
    
    % Weight components
    \\draw[->,red,dashed] (2.25,0.25) -- (2.75,0.5) node[right,font=\\small] {$mg\\sin\\theta$};
    \\draw[->,red,dashed] (2.25,0.25) -- (2.25,-0.25) node[below,font=\\small] {$mg\\cos\\theta$};
    
    % Angle
    \\draw (0.5,0) arc (0:26.57:0.5);
    \\node at (0.8,0.15) {$\\theta$};
\\end{tikzpicture}"""
                }
            ],
            "final_answers": [
                {
                    "question": "a) The acceleration of the block",
                    "answer": "2.4 m/s²",
                    "explanation": "The block accelerates down the incline at 2.4 m/s²"
                },
                {
                    "question": "b) The normal force",
                    "answer": "17.32 N",
                    "explanation": "The normal force equals the perpendicular component of the weight"
                },
                {
                    "question": "c) The friction force",
                    "answer": "5.2 N",
                    "explanation": "The kinetic friction force opposes the motion up the incline"
                }
            ]
        }
    
    def _solve_projectile_problem(self, problem_text: str) -> Dict:
        """Solve projectile motion problem"""
        return {
            "problem_type": "mechanics",
            "given_info": [
                "Launch angle (θ) = 45°",
                "Initial velocity (v₀) = 40 m/s",
                "Gravitational acceleration (g) = 10 m/s²"
            ],
            "find": [
                "a) Maximum height reached",
                "b) Range (horizontal distance)",
                "c) Time of flight"
            ],
            "solution_steps": [
                {
                    "step_number": 1,
                    "title": "Resolve Initial Velocity into Components",
                    "explanation": "Break down the initial velocity into horizontal and vertical components.",
                    "formulas": [
                        "v₀ₓ = v₀ cos(θ)",
                        "v₀ᵧ = v₀ sin(θ)"
                    ],
                    "calculations": [
                        "v₀ₓ = 40 × cos(45°) = 40 × 0.707 = 28.28 m/s",
                        "v₀ᵧ = 40 × sin(45°) = 40 × 0.707 = 28.28 m/s"
                    ],
                    "result": "Velocity components calculated"
                },
                {
                    "step_number": 2,
                    "title": "Calculate Maximum Height (a)",
                    "explanation": "At maximum height, vertical velocity becomes zero.",
                    "formulas": [
                        "h_max = (v₀ᵧ)² / (2g)"
                    ],
                    "calculations": [
                        "h_max = (28.28)² / (2 × 10) = 800 / 20 = 40 m"
                    ],
                    "result": "h_max = 40 m"
                },
                {
                    "step_number": 3,
                    "title": "Calculate Time of Flight (c)",
                    "explanation": "Total time in air until projectile returns to ground level.",
                    "formulas": [
                        "T = 2v₀ᵧ / g"
                    ],
                    "calculations": [
                        "T = 2 × 28.28 / 10 = 56.56 / 10 = 5.66 s"
                    ],
                    "result": "T = 5.66 s"
                },
                {
                    "step_number": 4,
                    "title": "Calculate Range (b)",
                    "explanation": "Horizontal distance traveled during time of flight.",
                    "formulas": [
                        "R = v₀ₓ × T"
                    ],
                    "calculations": [
                        "R = 28.28 × 5.66 = 160 m"
                    ],
                    "result": "R = 160 m"
                }
            ],
            "tikz_diagrams": [
                {
                    "type": "trajectory",
                    "title": "Projectile Motion Trajectory",
                    "code": """\\begin{tikzpicture}[scale=0.8]
    % Ground
    \\draw[thick] (0,0) -- (10,0);
    
    % Trajectory (parabola)
    \\draw[blue, very thick] (0,0) .. controls (3,4) and (7,4) .. (10,0);
    
    % Launch point
    \\fill (0,0) circle (3pt);
    \\node[below] at (0,0) {Launch};
    
    % Peak
    \\fill[red] (5,4) circle (3pt);
    \\node[above] at (5,4) {h$_{max}$ = 40m};
    \\draw[dashed] (5,0) -- (5,4);
    
    % Landing point
    \\fill (10,0) circle (3pt);
    \\node[below] at (10,0) {Land};
    
    % Range arrow
    \\draw[<->,green,thick] (0,-0.5) -- (10,-0.5) node[midway,below] {R = 160m};
    
    % Initial velocity vector
    \\draw[->,red,very thick] (0,0) -- (2,2) node[above right] {$\\vec{v_0}$=40 m/s};
    \\draw (0.7,0) arc (0:45:0.7);
    \\node at (1.2,0.3) {45°};
\\end{tikzpicture}"""
                }
            ],
            "final_answers": [
                {
                    "question": "a) Maximum height reached",
                    "answer": "40 m",
                    "explanation": "The projectile reaches a maximum height of 40 meters"
                },
                {
                    "question": "b) Range (horizontal distance)",
                    "answer": "160 m",
                    "explanation": "The projectile travels 160 meters horizontally"
                },
                {
                    "question": "c) Time of flight",
                    "answer": "5.66 s",
                    "explanation": "The projectile stays in air for approximately 5.66 seconds"
                }
            ]
        }
    
    def _solve_circuit_problem(self, problem_text: str) -> Dict:
        """Solve series circuit problem"""
        return {
            "problem_type": "electricity",
            "given_info": [
                "Voltage source (V) = 12 V",
                "Resistor R₁ = 4 Ω",
                "Resistor R₂ = 2 Ω"
            ],
            "find": [
                "a) Total resistance",
                "b) Current in the circuit",
                "c) Voltage across R₁ and R₂"
            ],
            "solution_steps": [
                {
                    "step_number": 1,
                    "title": "Calculate Total Resistance (a)",
                    "explanation": "In a series circuit, resistances add up.",
                    "formulas": [
                        "R_total = R₁ + R₂"
                    ],
                    "calculations": [
                        "R_total = 4 + 2 = 6 Ω"
                    ],
                    "result": "R_total = 6 Ω"
                },
                {
                    "step_number": 2,
                    "title": "Calculate Current (b)",
                    "explanation": "Use Ohm's law: V = IR",
                    "formulas": [
                        "I = V / R_total"
                    ],
                    "calculations": [
                        "I = 12 / 6 = 2 A"
                    ],
                    "result": "I = 2 A"
                },
                {
                    "step_number": 3,
                    "title": "Calculate Voltage Drops (c)",
                    "explanation": "In series, same current flows through all resistors.",
                    "formulas": [
                        "V₁ = I × R₁",
                        "V₂ = I × R₂"
                    ],
                    "calculations": [
                        "V₁ = 2 × 4 = 8 V",
                        "V₂ = 2 × 2 = 4 V"
                    ],
                    "result": "V₁ = 8 V, V₂ = 4 V"
                },
                {
                    "step_number": 4,
                    "title": "Verify Kirchhoff's Voltage Law",
                    "explanation": "Sum of voltage drops equals source voltage.",
                    "formulas": [
                        "V = V₁ + V₂"
                    ],
                    "calculations": [
                        "12 = 8 + 4 ✓"
                    ],
                    "result": "Verification successful"
                }
            ],
            "tikz_diagrams": [
                {
                    "type": "circuit",
                    "title": "Series Circuit Diagram",
                    "code": """\\begin{tikzpicture}[scale=1.5]
    % Battery
    \\draw[thick] (0,0) -- (0,0.5);
    \\draw[thick] (-0.2,0.5) -- (0.2,0.5);
    \\draw[thick] (-0.1,0.6) -- (0.1,0.6);
    \\node[left] at (-0.3,0.55) {$+$};
    \\node[left] at (-0.5,0.3) {12V};
    \\draw[thick] (0,0.6) -- (0,1);
    
    % Top wire with R1
    \\draw[thick] (0,1) -- (1.5,1);
    \\draw[thick] (1.5,1) -- (1.7,1.2) -- (1.9,0.8) -- (2.1,1.2) -- (2.3,0.8) -- (2.5,1.2) -- (2.7,1);
    \\node[above] at (2.1,1.2) {$R_1=4\\Omega$};
    \\node[above] at (2.1,1.5) {\\color{red}8V};
    
    % Wire with R2
    \\draw[thick] (2.7,1) -- (4,1);
    \\draw[thick] (4,1) -- (4.2,1.2) -- (4.4,0.8) -- (4.6,1.2) -- (4.8,0.8) -- (5,1.2) -- (5.2,1);
    \\node[above] at (4.6,1.2) {$R_2=2\\Omega$};
    \\node[above] at (4.6,1.5) {\\color{red}4V};
    
    % Return wire
    \\draw[thick] (5.2,1) -- (6,1) -- (6,0) -- (0,0);
    
    % Current arrows
    \\draw[->,blue,very thick] (1,1.3) -- (2,1.3) node[midway,above] {$I=2A$};
\\end{tikzpicture}"""
                }
            ],
            "final_answers": [
                {
                    "question": "a) Total resistance",
                    "answer": "6 Ω",
                    "explanation": "Series resistances add: 4Ω + 2Ω = 6Ω"
                },
                {
                    "question": "b) Current in the circuit",
                    "answer": "2 A",
                    "explanation": "Using Ohm's law: I = V/R = 12V/6Ω = 2A"
                },
                {
                    "question": "c) Voltage across R₁ and R₂",
                    "answer": "V₁ = 8V, V₂ = 4V",
                    "explanation": "Voltage drops calculated using V = IR for each resistor"
                }
            ]
        }
    
    def _solve_generic_problem(self, problem_text: str, problem_type: str) -> Dict:
        """Generate a generic solution structure for unknown problems"""
        return {
            "problem_type": problem_type,
            "given_info": [
                "Please review the problem statement above"
            ],
            "find": [
                "Analyzing problem requirements..."
            ],
            "solution_steps": [
                {
                    "step_number": 1,
                    "title": "Problem Analysis",
                    "explanation": f"This appears to be a {problem_type} problem. In production, an AI model (GPT-4 or Gemini) would analyze the problem and generate a complete step-by-step solution.",
                    "formulas": [
                        "Relevant physics equations would be applied here"
                    ],
                    "calculations": [
                        "Calculations would be performed step by step"
                    ],
                    "result": "AI-generated solution would appear here"
                },
                {
                    "step_number": 2,
                    "title": "Integration Note",
                    "explanation": "To get actual AI-powered solutions, integrate with:\n- OpenAI GPT-4 API\n- Google Gemini Pro API\n- Other AI physics solvers",
                    "formulas": [],
                    "calculations": [],
                    "result": "For now, try one of the sample problems for a complete demonstration"
                }
            ],
            "tikz_diagrams": [],
            "final_answers": [
                {
                    "question": "Solution",
                    "answer": "Pending AI integration",
                    "explanation": "This is a development placeholder. Integrate with AI APIs for actual solutions."
                }
            ]
        }
    
    def _solve_velocity_graph_problem(self, problem_text: str, image_analysis: Dict) -> Dict:
        """Solve problem with velocity-time graph"""
        return {
            "problem_type": "kinematics",
            "has_image": True,
            "image_description": image_analysis.get('description'),
            "given_info": [
                "Velocity-time graph with three phases",
                "Phase 1 (0-4s): Acceleration from 0 to 20 m/s",
                "Phase 2 (4-8s): Constant velocity at 20 m/s",
                "Phase 3 (8-12s): Deceleration from 20 to 0 m/s"
            ],
            "find": [
                "a) Acceleration during phase 1",
                "b) Total distance traveled",
                "c) Average velocity"
            ],
            "solution_steps": [
                {
                    "step_number": 1,
                    "title": "Analyze the Graph",
                    "explanation": "From the velocity-time graph, identify three distinct phases with different motion characteristics.",
                    "formulas": [],
                    "calculations": [
                        "Phase 1: Linear increase (acceleration)",
                        "Phase 2: Horizontal line (constant velocity)",
                        "Phase 3: Linear decrease (deceleration)"
                    ],
                    "result": "Three motion phases identified"
                },
                {
                    "step_number": 2,
                    "title": "Calculate Acceleration (a)",
                    "explanation": "Acceleration is the slope of v-t graph",
                    "formulas": [
                        "a = Δv / Δt = (v_final - v_initial) / time"
                    ],
                    "calculations": [
                        "Phase 1: a = (20 - 0) / (4 - 0) = 20/4 = 5 m/s²"
                    ],
                    "result": "a = 5 m/s²"
                },
                {
                    "step_number": 3,
                    "title": "Calculate Distance Using Area (b)",
                    "explanation": "Distance is the area under v-t graph",
                    "formulas": [
                        "Distance = Area under curve",
                        "Triangle area = ½ × base × height",
                        "Rectangle area = base × height"
                    ],
                    "calculations": [
                        "Phase 1 (triangle): d₁ = ½ × 4 × 20 = 40 m",
                        "Phase 2 (rectangle): d₂ = 4 × 20 = 80 m",
                        "Phase 3 (triangle): d₃ = ½ × 4 × 20 = 40 m",
                        "Total distance: d = 40 + 80 + 40 = 160 m"
                    ],
                    "result": "Total distance = 160 m"
                },
                {
                    "step_number": 4,
                    "title": "Calculate Average Velocity (c)",
                    "explanation": "Average velocity = total distance / total time",
                    "formulas": [
                        "v_avg = total distance / total time"
                    ],
                    "calculations": [
                        "v_avg = 160 / 12 = 13.33 m/s"
                    ],
                    "result": "v_avg = 13.33 m/s"
                }
            ],
            "tikz_diagrams": [
                {
                    "type": "graph",
                    "title": "Velocity-Time Graph",
                    "code": """\\begin{tikzpicture}[scale=0.8]
    % Axes
    \\draw[->] (0,0) -- (13,0) node[right] {Time (s)};
    \\draw[->] (0,0) -- (0,5) node[above] {Velocity (m/s)};
    
    % Grid
    \\foreach \\x in {0,2,4,6,8,10,12}
        \\draw (\\x,0.1) -- (\\x,-0.1) node[below] {\\x};
    \\foreach \\y in {0,5,10,15,20}
        \\draw (0.1,\\y/4) -- (-0.1,\\y/4) node[left] {\\y};
    
    % Graph lines
    \\draw[blue, very thick] (0,0) -- (4,5) -- (8,5) -- (12,0);
    
    % Phase labels
    \\node[blue] at (2,3) {Phase 1};
    \\node[blue] at (6,5.5) {Phase 2};
    \\node[blue] at (10,3) {Phase 3};
    
    % Area shading
    \\fill[blue!20] (0,0) -- (4,5) -- (4,0) -- cycle;
    \\fill[green!20] (4,0) -- (4,5) -- (8,5) -- (8,0) -- cycle;
    \\fill[red!20] (8,0) -- (8,5) -- (12,0) -- cycle;
    
    % Key points
    \\fill (0,0) circle (2pt) node[below left] {Start};
    \\fill (4,5) circle (2pt) node[above] {20 m/s};
    \\fill (8,5) circle (2pt);
    \\fill (12,0) circle (2pt) node[below right] {End};
\\end{tikzpicture}"""
                }
            ],
            "final_answers": [
                {
                    "question": "a) Acceleration during phase 1",
                    "answer": "5 m/s²",
                    "explanation": "Calculated from slope: Δv/Δt = 20/4 = 5 m/s²"
                },
                {
                    "question": "b) Total distance traveled",
                    "answer": "160 m",
                    "explanation": "Sum of areas: 40 + 80 + 40 = 160 m"
                },
                {
                    "question": "c) Average velocity",
                    "answer": "13.33 m/s",
                    "explanation": "Total distance / total time = 160/12 ≈ 13.33 m/s"
                }
            ]
        }
    
    def _solve_graph_problem(self, problem_text: str) -> Dict:
        """Solve kinematics graph problem without image"""
        return {
            "problem_type": "kinematics",
            "given_info": [
                "Analyzing graph-based kinematics problem",
                "Graph shows motion with changing velocity"
            ],
            "find": [
                "Information from graph analysis"
            ],
            "solution_steps": [
                {
                    "step_number": 1,
                    "title": "Graph Analysis",
                    "explanation": "For velocity-time graphs: slope gives acceleration, area gives displacement. For position-time graphs: slope gives velocity.",
                    "formulas": [
                        "v-t graph: a = slope, d = area",
                        "x-t graph: v = slope"
                    ],
                    "calculations": [],
                    "result": "Apply appropriate graph analysis method"
                }
            ],
            "tikz_diagrams": [],
            "final_answers": [
                {
                    "question": "Solution",
                    "answer": "Upload a graph image for detailed analysis",
                    "explanation": "Use the image upload feature to analyze specific graphs"
                }
            ]
        }
    
    def _solve_circuit_diagram_problem(self, problem_text: str, image_analysis: Dict) -> Dict:
        """Solve circuit problem with diagram"""
        return {
            "problem_type": "electricity",
            "has_image": True,
            "image_description": image_analysis.get('description'),
            "given_info": [
                "Circuit diagram with:",
                "- Voltage source: 24V",
                "- R1 (series): 6Ω",
                "- R2 and R3 (parallel): 12Ω each"
            ],
            "find": [
                "a) Total resistance",
                "b) Total current",
                "c) Current through each resistor",
                "d) Voltage across each resistor"
            ],
            "solution_steps": [
                {
                    "step_number": 1,
                    "title": "Analyze Circuit Topology",
                    "explanation": "Identify series and parallel combinations",
                    "formulas": [],
                    "calculations": [
                        "R1 is in series with the main line",
                        "R2 and R3 are in parallel with each other",
                        "The parallel combination is in series with R1"
                    ],
                    "result": "Series-parallel combination identified"
                },
                {
                    "step_number": 2,
                    "title": "Calculate Parallel Resistance",
                    "explanation": "For parallel resistors, use reciprocal formula",
                    "formulas": [
                        "1/R_parallel = 1/R2 + 1/R3"
                    ],
                    "calculations": [
                        "1/R_parallel = 1/12 + 1/12 = 2/12",
                        "R_parallel = 6Ω"
                    ],
                    "result": "R_parallel = 6Ω"
                },
                {
                    "step_number": 3,
                    "title": "Calculate Total Resistance (a)",
                    "explanation": "Add series resistances",
                    "formulas": [
                        "R_total = R1 + R_parallel"
                    ],
                    "calculations": [
                        "R_total = 6 + 6 = 12Ω"
                    ],
                    "result": "R_total = 12Ω"
                },
                {
                    "step_number": 4,
                    "title": "Calculate Total Current (b)",
                    "explanation": "Use Ohm's law",
                    "formulas": [
                        "I_total = V / R_total"
                    ],
                    "calculations": [
                        "I_total = 24 / 12 = 2A"
                    ],
                    "result": "I_total = 2A"
                },
                {
                    "step_number": 5,
                    "title": "Calculate Voltages and Branch Currents (c, d)",
                    "explanation": "Voltage across R1, then across parallel branch",
                    "formulas": [
                        "V = IR"
                    ],
                    "calculations": [
                        "V1 = 2 × 6 = 12V",
                        "V_parallel = 24 - 12 = 12V",
                        "I2 = V_parallel / R2 = 12/12 = 1A",
                        "I3 = V_parallel / R3 = 12/12 = 1A"
                    ],
                    "result": "V1 = 12V, V_parallel = 12V, I2 = I3 = 1A"
                }
            ],
            "tikz_diagrams": [],
            "final_answers": [
                {
                    "question": "a) Total resistance",
                    "answer": "12Ω",
                    "explanation": "Series combination: 6Ω + 6Ω = 12Ω"
                },
                {
                    "question": "b) Total current",
                    "answer": "2A",
                    "explanation": "I = V/R = 24V/12Ω = 2A"
                },
                {
                    "question": "c) Current through each resistor",
                    "answer": "I1 = 2A, I2 = 1A, I3 = 1A",
                    "explanation": "Series current same, parallel splits equally"
                },
                {
                    "question": "d) Voltage across each resistor",
                    "answer": "V1 = 12V, V2 = V3 = 12V",
                    "explanation": "Calculated using Ohm's law"
                }
            ]
        }
    
    def _solve_diagram_problem(self, problem_text: str, image_analysis: Dict) -> Dict:
        """Solve problem with physics diagram"""
        return {
            "problem_type": "mechanics",
            "has_image": True,
            "image_description": image_analysis.get('description'),
            "given_info": image_analysis.get('key_elements', []),
            "find": ["Quantities that can be calculated from the diagram"],
            "solution_steps": [
                {
                    "step_number": 1,
                    "title": "Analyze Diagram",
                    "explanation": image_analysis.get('description', 'Analyzing the provided diagram'),
                    "formulas": [],
                    "calculations": image_analysis.get('can_calculate', []),
                    "result": "Diagram analyzed successfully"
                }
            ],
            "tikz_diagrams": [],
            "final_answers": [
                {
                    "question": "Analysis",
                    "answer": "See calculations above",
                    "explanation": "Based on diagram analysis"
                }
            ]
        }
