# SITREP Backend API
# FastAPI server for intelligence briefing synthesis and PDF generation

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pathlib import Path
from datetime import datetime, timezone
import json
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Application version. Bump on each deploy so the running build can be
# identified via GET / (used to confirm a Railway redeploy is live).
APP_VERSION = "0.20.4"

# Initialize Supabase client (optional for local dev)
try:
    from database.supabase_client import SupabaseClient
    supabase = SupabaseClient()
    USE_SUPABASE = True
    logger.info("Supabase client initialized successfully")
except Exception as e:
    USE_SUPABASE = False
    supabase = None
    logger.warning(f"Supabase not available, using file-based storage: {e}")

# Initialize scheduler
from scheduler import BriefingScheduler
scheduler = None

app = FastAPI(
    title="SITREP API",
    description="AI-powered intelligence briefing generation and synthesis",
    version=APP_VERSION
)

# CORS middleware for mobile app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Initialize scheduler on app startup"""
    global scheduler
    # Get Railway URL or fallback to localhost
    railway_url = os.getenv("RAILWAY_PUBLIC_DOMAIN")
    if railway_url:
        api_url = f"https://{railway_url}"
    else:
        api_url = "http://localhost:8000"

    scheduler = BriefingScheduler(api_base_url=api_url)
    scheduler.start()
    logger.info(f"Application started - scheduler configured for {api_url}")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on app shutdown"""
    global scheduler
    if scheduler:
        scheduler.shutdown()
    logger.info("Application shutdown complete")

@app.get("/")
async def root():
    """Root endpoint with scheduler status"""
    storage_mode = "Supabase" if USE_SUPABASE else "File-based"

    scheduler_status = "Not initialized"
    next_run = None
    if scheduler and scheduler.scheduler.running:
        scheduler_status = "Running - Daily at 06:00 UTC"
        job = scheduler.scheduler.get_job('daily_briefing_pipeline')
        if job:
            next_run = job.next_run_time.isoformat() if job.next_run_time else None

    return {
        "message": f"SITREP API v{APP_VERSION}",
        "version": APP_VERSION,
        "storage": storage_mode,
        "scheduler": scheduler_status,
        "next_scheduled_run": next_run
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "ok",
        "version": "0.10.0",
        "supabase_enabled": USE_SUPABASE
    }

@app.post("/scrape")
async def scrape_sources(region: str = "Europe/Africa", days: int = 7):
    """
    Scrape intelligence sources for a specific region.

    Args:
        region: Geographic region to scrape (default: Europe/Africa)
        days: Number of days to look back (default: 7)

    Returns:
        Scraping status and article count
    """
    try:
        from scrapers.orchestrator import ScraperOrchestrator

        orchestrator = ScraperOrchestrator()
        results = await orchestrator.scrape_all_sources(days=days)

        # Save results to JSON files
        orchestrator.save_all_results(results)

        # Get summary statistics
        summary = orchestrator.get_summary(results)

        return {
            "status": "success",
            "total_articles": summary["total_articles"],
            "by_source": summary["by_source"],
            "by_region": summary["by_region"],
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")


@app.post("/synthesize")
async def synthesize_briefing(region: str = "Europe/Africa"):
    """
    Generate BLUF briefing from scraped articles.

    Args:
        region: Geographic region to synthesize (default: Europe/Africa)

    Returns:
        Generated briefing and metadata
    """
    try:
        from synthesis.bluf_synthesizer import BLUFSynthesizer

        # Find latest scraped articles
        scraped_dir = Path("data/scraped")
        if not scraped_dir.exists():
            raise HTTPException(status_code=404, detail="No scraped articles found")

        # Load all scraped articles
        all_articles = []
        for json_file in scraped_dir.glob("*.json"):
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Handle both formats: list of articles or dict with 'articles' key
                if isinstance(data, list):
                    all_articles.extend(data)
                elif isinstance(data, dict) and 'articles' in data:
                    all_articles.extend(data['articles'])
                else:
                    raise ValueError(f"Unexpected JSON format in {json_file.name}")

        if not all_articles:
            raise HTTPException(status_code=404, detail="No articles to synthesize")

        # Synthesize briefing
        synthesizer = BLUFSynthesizer()
        briefing = await synthesizer.synthesize_region(all_articles, region)

        # Save briefing to disk
        briefing_dir = Path("data/briefings")
        briefing_dir.mkdir(parents=True, exist_ok=True)

        # Create filename with region and timestamp
        region_slug = region.lower().replace(' ', '_').replace('/', '_')
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        briefing_file = briefing_dir / f"{region_slug}_{timestamp}.json"

        with open(briefing_file, 'w', encoding='utf-8') as f:
            json.dump(briefing, f, indent=2, ensure_ascii=False)

        return {
            "status": "success",
            "region": region,
            "briefing": briefing,
            "source_articles": len(all_articles),
            "briefing_file": str(briefing_file),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Synthesis failed: {str(e)}")


@app.get("/briefing/latest")
async def get_latest_briefing(region: str = "Europe/Africa"):
    """
    Get latest cached briefing for a region.

    Tries Supabase first, falls back to file-based storage.

    Args:
        region: Geographic region (default: Europe/Africa)

    Returns:
        Latest briefing JSON
    """
    try:
        # Try Supabase first if available
        if USE_SUPABASE and supabase:
            try:
                supabase_briefing = await supabase.get_latest_briefing(region)
                if supabase_briefing:
                    return {
                        "status": "success",
                        "region": region,
                        "briefing": supabase_briefing["briefing_data"],
                        "source": "supabase",
                        "generated_at": supabase_briefing["generated_at"],
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    }
            except Exception as e:
                logger.warning(f"Supabase lookup failed, falling back to files: {e}")

        # Fall back to file-based storage
        briefing_dir = Path("data/briefings")
        if not briefing_dir.exists():
            raise HTTPException(status_code=404, detail="No briefings available")

        region_slug = region.lower().replace(' ', '_').replace('/', '_')
        briefing_files = list(briefing_dir.glob(f"{region_slug}_*.json"))

        if not briefing_files:
            raise HTTPException(status_code=404, detail=f"No briefings found for {region}")

        latest_briefing = max(briefing_files, key=lambda p: p.stat().st_mtime)

        # Load and return briefing
        with open(latest_briefing, 'r', encoding='utf-8') as f:
            briefing = json.load(f)

        return {
            "status": "success",
            "region": region,
            "briefing": briefing,
            "source": "file",
            "source_file": str(latest_briefing.name),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving briefing: {str(e)}")

@app.get("/briefing/global")
async def get_global_briefing():
    """
    Get the latest cached cross-regional global intelligence briefing.

    This briefing synthesizes articles from all regions into a thematic
    cross-regional analysis, identifying connections between theaters.

    Returns:
        Global briefing JSON
    """
    try:
        # Try Supabase first
        if USE_SUPABASE and supabase:
            try:
                supabase_briefing = await supabase.get_latest_briefing("Global")
                if supabase_briefing:
                    return {
                        "status": "success",
                        "region": "Global",
                        "briefing": supabase_briefing["briefing_data"],
                        "source": "supabase",
                        "timestamp": datetime.now(timezone.utc).isoformat()
                    }
            except Exception as e:
                logger.warning(f"Supabase global lookup failed, falling back to files: {e}")

        # Fall back to file-based storage
        briefing_dir = Path("data/briefings")
        if not briefing_dir.exists():
            raise HTTPException(status_code=404, detail="No briefings available")

        briefing_files = list(briefing_dir.glob("global_*.json"))
        if not briefing_files:
            raise HTTPException(status_code=404, detail="No global briefing found. Run /synthesize/global to generate one.")

        latest = max(briefing_files, key=lambda p: p.stat().st_mtime)
        with open(latest, 'r', encoding='utf-8') as f:
            briefing = json.load(f)

        return {
            "status": "success",
            "region": "Global",
            "briefing": briefing,
            "source": "file",
            "source_file": str(latest.name),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving global briefing: {str(e)}")


@app.post("/synthesize/global")
async def synthesize_global_briefing():
    """
    Generate a cross-regional global intelligence briefing from all scraped articles.

    Synthesizes thematic cross-regional analysis identifying connections between theaters.

    Returns:
        Generated global briefing and metadata
    """
    try:
        from synthesis.bluf_synthesizer import BLUFSynthesizer

        scraped_dir = Path("data/scraped")
        if not scraped_dir.exists():
            raise HTTPException(status_code=404, detail="No scraped articles found. Run /scrape first.")

        all_articles = []
        for json_file in scraped_dir.glob("*.json"):
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    all_articles.extend(data)
                elif isinstance(data, dict) and 'articles' in data:
                    all_articles.extend(data['articles'])

        if not all_articles:
            raise HTTPException(status_code=404, detail="No articles to synthesize")

        synthesizer = BLUFSynthesizer()
        briefing = await synthesizer.synthesize_global(all_articles)

        # Save to file
        briefing_dir = Path("data/briefings")
        briefing_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        briefing_file = briefing_dir / f"global_{timestamp}.json"

        with open(briefing_file, 'w', encoding='utf-8') as f:
            json.dump(briefing, f, indent=2, ensure_ascii=False)

        return {
            "status": "success",
            "region": "Global",
            "briefing": briefing,
            "source_articles": len(all_articles),
            "briefing_file": str(briefing_file),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Global synthesis failed: {str(e)}")


@app.get("/briefing/latest/pdf")
async def get_latest_pdf(region: str = "Europe/Africa"):
    """
    Get latest briefing as PDF for a specific region.

    Args:
        region: Geographic region (default: Europe/Africa). Use "Global" for cross-regional briefing.

    Returns PDF file for download.
    """
    try:
        # Find latest PDF in data/pdfs/
        pdf_dir = Path("data/pdfs")
        if not pdf_dir.exists():
            raise HTTPException(status_code=404, detail="No PDFs available")

        # Map region to PDF filename pattern
        region_slug = region.lower().replace(' ', '_').replace('/', '_')

        # Find PDFs matching this region
        pdf_pattern = f"{region_slug}_*.pdf"
        pdf_files = list(pdf_dir.glob(pdf_pattern))

        if not pdf_files:
            raise HTTPException(status_code=404, detail=f"No PDF found for region: {region}")

        # Get most recent PDF for this region
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
        from pdf_generation.pdf_generator_v2 import PDFGeneratorV2 as PDFGenerator

        # Find latest briefing JSON for region
        briefing_dir = Path("data/briefings")
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


@app.post("/pipeline/run-weekly")
async def run_weekly_pipeline():
    """
    Execute weekly briefing generation pipeline.

    Orchestrates:
    1. Scrape all sources
    2. Synthesize briefings for all 4 regions
    3. Generate PDFs for all 4 regions
    4. Cache briefings to Supabase (if enabled)

    Returns:
        Pipeline execution summary
    """
    try:
        logger.info("Starting weekly briefing pipeline")

        regions = ["Middle East", "Indo-Pacific", "Europe/Africa", "Western Hemisphere"]
        pipeline_results = {
            "status": "success",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "regions_processed": [],
            "errors": []
        }

        # Step 1: Scrape sources
        logger.info("Step 1: Scraping sources")
        try:
            from scrapers.orchestrator import ScraperOrchestrator
            orchestrator = ScraperOrchestrator()
            scrape_results = await orchestrator.scrape_all_sources(days=7)
            orchestrator.save_all_results(scrape_results)
            summary = orchestrator.get_summary(scrape_results)
            pipeline_results["scraping"] = {
                "total_articles": summary["total_articles"],
                "by_source": summary["by_source"]
            }
            logger.info(f"Scraping complete: {summary['total_articles']} articles")
        except Exception as e:
            error_msg = f"Scraping failed: {str(e)}"
            logger.error(error_msg)
            pipeline_results["errors"].append(error_msg)
            return JSONResponse(status_code=500, content=pipeline_results)

        # Step 2 & 3: Synthesize briefings and generate PDFs for each region
        for region in regions:
            try:
                logger.info(f"Processing region: {region}")

                # Synthesize briefing
                from synthesis.bluf_synthesizer import BLUFSynthesizer
                from pdf_generation.pdf_generator_v2 import PDFGeneratorV2 as PDFGenerator

                # Load scraped articles
                scraped_dir = Path("data/scraped")
                all_articles = []
                for json_file in scraped_dir.glob("*.json"):
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            all_articles.extend(data)
                        elif isinstance(data, dict) and 'articles' in data:
                            all_articles.extend(data['articles'])

                # Synthesize
                synthesizer = BLUFSynthesizer()
                briefing = await synthesizer.synthesize_region(all_articles, region)

                # Save briefing JSON (file-based backup)
                briefing_dir = Path("data/briefings")
                briefing_dir.mkdir(parents=True, exist_ok=True)
                region_slug = region.lower().replace(' ', '_').replace('/', '_')
                timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
                briefing_file = briefing_dir / f"{region_slug}_{timestamp}.json"

                with open(briefing_file, 'w', encoding='utf-8') as f:
                    json.dump(briefing, f, indent=2, ensure_ascii=False)

                # Generate PDF
                generator = PDFGenerator()
                pdf_path = generator.generate_pdf(briefing)

                # Cache to Supabase if available
                if USE_SUPABASE and supabase:
                    try:
                        await supabase.save_briefing(
                            region=region,
                            briefing_data=briefing,
                            pdf_url=None  # PDFs stored locally for now
                        )
                        logger.info(f"Cached {region} to Supabase")
                    except Exception as e:
                        logger.warning(f"Supabase caching failed for {region}: {e}")

                pipeline_results["regions_processed"].append({
                    "region": region,
                    "briefing_file": str(briefing_file),
                    "pdf_path": pdf_path,
                    "sections": len(briefing.get("sections", [])),
                    "article_count": briefing.get("article_count", 0)
                })

                logger.info(f"Completed {region}: {len(briefing.get('sections', []))} sections")

            except Exception as e:
                error_msg = f"{region} processing failed: {str(e)}"
                logger.error(error_msg)
                pipeline_results["errors"].append(error_msg)

        # Step 4: Generate Global cross-regional briefing
        try:
            logger.info("Step 4: Generating global cross-regional briefing")
            from synthesis.bluf_synthesizer import BLUFSynthesizer

            scraped_dir = Path("data/scraped")
            all_articles = []
            for json_file in scraped_dir.glob("*.json"):
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        all_articles.extend(data)
                    elif isinstance(data, dict) and 'articles' in data:
                        all_articles.extend(data['articles'])

            synthesizer = BLUFSynthesizer()
            global_briefing = await synthesizer.synthesize_global(all_articles)

            briefing_dir = Path("data/briefings")
            briefing_dir.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
            global_file = briefing_dir / f"global_{timestamp}.json"

            with open(global_file, 'w', encoding='utf-8') as f:
                json.dump(global_briefing, f, indent=2, ensure_ascii=False)

            # Generate Global PDF
            from pdf_generation.pdf_generator_v2 import PDFGeneratorV2 as PDFGenerator
            generator = PDFGenerator()
            global_pdf_path = generator.generate_pdf(global_briefing)
            logger.info(f"Generated Global PDF: {global_pdf_path}")

            if USE_SUPABASE and supabase:
                try:
                    await supabase.save_briefing(
                        region="Global",
                        briefing_data=global_briefing,
                        pdf_url=None
                    )
                    logger.info("Cached Global briefing to Supabase")
                except Exception as e:
                    logger.warning(f"Supabase caching failed for Global: {e}")

            pipeline_results["global_briefing"] = {
                "file": str(global_file),
                "pdf_path": global_pdf_path,
                "sections": len(global_briefing.get("sections", [])),
                "article_count": global_briefing.get("article_count", 0)
            }
            logger.info(f"Global briefing complete: {len(global_briefing.get('sections', []))} sections")

        except Exception as e:
            error_msg = f"Global briefing failed: {str(e)}"
            logger.error(error_msg)
            pipeline_results["errors"].append(error_msg)

        # Summary
        pipeline_results["total_regions"] = len(regions)
        pipeline_results["successful_regions"] = len(pipeline_results["regions_processed"])
        pipeline_results["failed_regions"] = len(pipeline_results["errors"])

        logger.info(f"Pipeline complete: {pipeline_results['successful_regions']}/{pipeline_results['total_regions']} regions")

        return pipeline_results

    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Pipeline execution failed: {str(e)}")


@app.get("/debug/supabase")
async def debug_supabase():
    """
    Test Supabase connection and show status.
    Returns connection status and sample data if available.
    """
    result = {
        "enabled": USE_SUPABASE,
        "client_initialized": supabase is not None,
        "briefings_count": 0,
        "sample_regions": []
    }

    if USE_SUPABASE and supabase:
        try:
            # Try to fetch all briefings
            all_briefings = await supabase.get_all_briefings()
            result["briefings_count"] = len(all_briefings)
            result["sample_regions"] = [b.get("region") for b in all_briefings]

            if all_briefings:
                result["sample_briefing"] = {
                    "region": all_briefings[0].get("region"),
                    "generated_at": all_briefings[0].get("generated_at"),
                    "article_count": all_briefings[0].get("briefing_data", {}).get("article_count", 0)
                }
        except Exception as e:
            result["error"] = str(e)

    return result


@app.post("/debug/upload-briefing")
async def upload_briefing_to_supabase(region: str):
    """
    Manually upload a briefing from filesystem to Supabase.
    Useful for debugging Supabase save issues.
    """
    if not USE_SUPABASE or not supabase:
        raise HTTPException(status_code=503, detail="Supabase not available")

    try:
        # Find latest briefing file for this region
        briefing_dir = Path("data/briefings")
        if not briefing_dir.exists():
            raise HTTPException(status_code=404, detail="No briefings directory found")

        region_slug = region.lower().replace(' ', '_').replace('/', '_')
        briefing_files = sorted(briefing_dir.glob(f"{region_slug}_*.json"), key=lambda p: p.stat().st_mtime, reverse=True)

        if not briefing_files:
            raise HTTPException(status_code=404, detail=f"No briefing files found for {region}")

        # Load latest briefing
        latest_file = briefing_files[0]
        with open(latest_file, 'r', encoding='utf-8') as f:
            briefing_data = json.load(f)

        # Upload to Supabase
        result = await supabase.save_briefing(
            region=region,
            briefing_data=briefing_data,
            pdf_url=None
        )

        return {
            "status": "success",
            "region": region,
            "file": str(latest_file),
            "uploaded_at": datetime.now(timezone.utc).isoformat(),
            "article_count": briefing_data.get("article_count", 0)
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
