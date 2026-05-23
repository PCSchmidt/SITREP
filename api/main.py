# SITREP Backend API
# FastAPI server for intelligence briefing synthesis and PDF generation

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pathlib import Path
import json

app = FastAPI(
    title="SITREP API",
    description="AI-powered intelligence briefing generation and synthesis",
    version="0.3.0"
)

# CORS middleware for mobile app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "SITREP API v0.0.1"}

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "ok", "version": "0.0.1"}

# Placeholder endpoints for future gates
@app.post("/scrape")
async def scrape_sources():
    """Scrape intelligence sources (v0.1)"""
    return {"message": "Scraping endpoint - to be implemented in v0.1"}

@app.post("/synthesize")
async def synthesize_briefing():
    """Generate BLUF briefing from articles (v0.2)"""
    return {"message": "Synthesis endpoint - to be implemented in v0.2"}

@app.get("/briefing/latest")
async def get_latest_briefing():
    """Get latest cached briefing (v0.5)"""
    return {"message": "Briefing endpoint - to be implemented in v0.5"}

@app.get("/briefing/latest/pdf")
async def get_latest_pdf():
    """
    Get latest briefing as PDF.

    Returns PDF file for download.
    """
    try:
        # Find latest PDF in data/pdfs/
        pdf_dir = Path("../data/pdfs")
        if not pdf_dir.exists():
            raise HTTPException(status_code=404, detail="No PDFs available")

        # Get most recent PDF
        pdf_files = list(pdf_dir.glob("*.pdf"))
        if not pdf_files:
            raise HTTPException(status_code=404, detail="No PDFs found")

        latest_pdf = max(pdf_files, key=lambda p: p.stat().st_mtime)

        # Return PDF file
        return FileResponse(
            path=str(latest_pdf),
            media_type="application/pdf",
            filename=latest_pdf.name
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving PDF: {str(e)}")


@app.post("/briefing/generate-pdf")
async def generate_pdf(region: str = "Europe/Africa"):
    """
    Generate PDF from latest briefing JSON.

    Args:
        region: Geographic region (default: Europe/Africa)

    Returns:
        Path to generated PDF
    """
    try:
        from pdf_generation.pdf_generator_reportlab import PDFGenerator

        # Find latest briefing JSON for region
        briefing_dir = Path("../data/briefings")
        region_slug = region.lower().replace(' ', '_').replace('/', '_')

        briefing_files = list(briefing_dir.glob(f"{region_slug}_*.json"))
        if not briefing_files:
            raise HTTPException(status_code=404, detail=f"No briefings found for {region}")

        latest_briefing = max(briefing_files, key=lambda p: p.stat().st_mtime)

        # Load briefing
        with open(latest_briefing, 'r', encoding='utf-8') as f:
            briefing = json.load(f)

        # Generate PDF
        generator = PDFGenerator()
        pdf_path = generator.generate_pdf(briefing)

        return {
            "status": "success",
            "pdf_path": pdf_path,
            "briefing_source": str(latest_briefing),
            "region": region
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")
