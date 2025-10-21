from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .config import settings
from .routers import (
    upload_router,
    convert_router,
    templates_router,
    render_router,
    export_router,
    solver_router
)
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Physics Diagram Converter API",
    description="Convert handwritten physics diagrams to digital TikZ diagrams using DaTikZv2",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload_router)
app.include_router(convert_router)
app.include_router(templates_router)
app.include_router(render_router)
app.include_router(export_router)
app.include_router(solver_router)

# Mount static files for outputs
app.mount("/api/outputs", StaticFiles(directory=settings.output_dir), name="outputs")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Physics Diagram Converter API",
        "version": "1.0.0",
        "description": "Convert handwritten physics diagrams to digital TikZ diagrams",
        "endpoints": {
            "upload": "/api/upload",
            "convert": "/api/convert",
            "templates": "/api/templates",
            "render": "/api/render",
            "export": "/api/export",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )
