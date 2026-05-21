# SITREP Backend API
# FastAPI server for intelligence briefing synthesis and PDF generation

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI(
    title="SITREP API",
    description="AI-powered intelligence briefing generation and synthesis",
    version="0.0.1"
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
    """Get latest briefing as PDF (v0.3)"""
    return {"message": "PDF endpoint - to be implemented in v0.3"}
