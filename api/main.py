# SITREP Backend API
# FastAPI server for intelligence briefing synthesis and PDF generation

from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pathlib import Path
from datetime import datetime, timezone
import json
import os
import logging
import secrets
from typing import Any, Dict, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SCRAPED_DIR = Path("data/scraped")
BRIEFING_DIR = Path("data/briefings")


ADMIN_TOKEN_ENV = "SITREP_ADMIN_TOKEN"
ADMIN_TOKEN_HEADER = "X-Admin-Token"


async def require_admin_token(request: Request, x_admin_token: str | None = Header(default=None)) -> None:
    """Protect pipeline and debug endpoints with a shared secret.

    Enforcement is opt-in so an existing deployment is never locked out
    unexpectedly: when SITREP_ADMIN_TOKEN is unset, the request is allowed and a
    warning is logged. Set SITREP_ADMIN_TOKEN on the host (and on every caller:
    the in-app scheduler, refresh_railway_briefings.py, and the GitHub Actions
    workflow) to require the X-Admin-Token header.
    """
    expected = (os.getenv(ADMIN_TOKEN_ENV) or "").strip()

    if not expected:
        logger.warning(
            "%s is not set: %s is unauthenticated. Set it to require the %s header.",
            ADMIN_TOKEN_ENV,
            request.url.path,
            ADMIN_TOKEN_HEADER,
        )
        return

    if x_admin_token is None:
        raise HTTPException(status_code=401, detail=f"Missing {ADMIN_TOKEN_HEADER} header")
    if not secrets.compare_digest(x_admin_token, expected):
        raise HTTPException(status_code=403, detail="Invalid admin token")


def _clear_json_files(directory: Path) -> int:
    """Remove stale JSON snapshots before writing the current run."""
    if not directory.exists():
        return 0

    removed = 0
    for json_file in directory.glob("*.json"):
        json_file.unlink(missing_ok=True)
        removed += 1
    return removed


def _flatten_scrape_results(scrape_results: Dict[str, List[Any]]) -> List[Dict[str, Any]]:
    """Normalize current-run scraper results into plain dicts for synthesis."""
    flattened: List[Dict[str, Any]] = []
    for articles in scrape_results.values():
        for article in articles:
            if hasattr(article, "to_dict"):
                flattened.append(article.to_dict())
            elif isinstance(article, dict):
                flattened.append(article)
    return flattened


def _load_latest_scraped_articles() -> List[Dict[str, Any]]:
    """Load only the latest scraped snapshot per source from disk."""
    if not SCRAPED_DIR.exists():
        return []

    latest_by_source: Dict[str, tuple[float, List[Dict[str, Any]]]] = {}
    for json_file in SCRAPED_DIR.glob("*.json"):
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if isinstance(data, list):
            articles = data
            source_name = json_file.stem
        elif isinstance(data, dict) and 'articles' in data:
            articles = data['articles']
            source_name = data.get('source') or json_file.stem
        else:
            raise ValueError(f"Unexpected JSON format in {json_file.name}")

        mtime = json_file.stat().st_mtime
        current = latest_by_source.get(source_name)
        if current is None or mtime > current[0]:
            latest_by_source[source_name] = (mtime, articles)

    all_articles: List[Dict[str, Any]] = []
    for _, articles in latest_by_source.values():
        all_articles.extend(articles)
    return all_articles


def _aggregate_freshness_blocks(freshness_blocks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Aggregate per-region freshness diagnostics into one summary."""
    valid_blocks = [block for block in freshness_blocks if block]
    if not valid_blocks:
        return {}

    newest_dates = [block.get("newest_article_date") for block in valid_blocks if block.get("newest_article_date")]
    oldest_dates = [block.get("oldest_article_date") for block in valid_blocks if block.get("oldest_article_date")]
    median_ages = [block.get("median_article_age_days") for block in valid_blocks if block.get("median_article_age_days") is not None]

    top_titles: List[str] = []
    for block in valid_blocks:
        for title in block.get("top_titles", []):
            if title and title not in top_titles:
                top_titles.append(title)
            if len(top_titles) == 5:
                break
        if len(top_titles) == 5:
            break

    return {
        "selected_count": sum(block.get("selected_count", 0) for block in valid_blocks),
        "newest_article_date": max(newest_dates) if newest_dates else None,
        "oldest_article_date": min(oldest_dates) if oldest_dates else None,
        "median_article_age_days": round(sum(median_ages) / len(median_ages), 2) if median_ages else None,
        "same_day_articles": sum(block.get("same_day_articles", 0) for block in valid_blocks),
        "within_48h_articles": sum(block.get("within_48h_articles", 0) for block in valid_blocks),
        "top_titles": top_titles,
    }

async def _load_briefing_for_pdf(region: str) -> "Dict[str, Any] | None":
    """Load the newest briefing for a region: Supabase first, then disk files."""
    if USE_SUPABASE and supabase:
        try:
            record = await supabase.get_latest_briefing(region)
            if record and record.get("briefing_data"):
                return record["briefing_data"]
        except Exception as e:
            logger.warning(f"Supabase briefing lookup for PDF failed: {e}")

    briefing_dir = Path("data/briefings")
    if not briefing_dir.exists():
        return None

    region_slug = region.lower().replace(' ', '_').replace('/', '_')
    briefing_files = list(briefing_dir.glob(f"{region_slug}_*.json"))
    if not briefing_files:
        return None

    latest = max(briefing_files, key=lambda p: p.stat().st_mtime)
    with open(latest, 'r', encoding='utf-8') as f:
        return json.load(f)


def _pdf_needs_refresh(pdf_path: "Path | None", briefing: Dict[str, Any]) -> bool:
    """True when there is no PDF yet, or the cached file predates the briefing."""
    if pdf_path is None or not pdf_path.exists():
        return True

    raw = briefing.get("generated_at")
    if not raw:
        return False

    try:
        generated_at = datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
    except ValueError:
        return False

    if generated_at.tzinfo is None:
        generated_at = generated_at.replace(tzinfo=timezone.utc)

    return pdf_path.stat().st_mtime < generated_at.timestamp()


def _stamp_generated_at(briefing: Dict[str, Any]) -> Dict[str, Any]:
    """Record when a briefing was produced.

    The synthesizer does not set this field, and the mobile client formats it
    directly: a briefing saved without `generated_at` throws in the client and the
    whole region disappears from the app ("No briefings available for this region").
    """
    if not briefing.get("generated_at"):
        briefing["generated_at"] = datetime.now(timezone.utc).isoformat()
    return briefing


# Application version. Bump on each deploy so the running build can be
# identified via GET / (used to confirm a Railway redeploy is live).
APP_VERSION = "0.21.10"

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
        "version": APP_VERSION,
        "supabase_enabled": USE_SUPABASE
    }

@app.post("/scrape", dependencies=[Depends(require_admin_token)])
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
        _clear_json_files(SCRAPED_DIR)
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


@app.post("/synthesize", dependencies=[Depends(require_admin_token)])
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
        if not SCRAPED_DIR.exists():
            raise HTTPException(status_code=404, detail="No scraped articles found")

        all_articles = _load_latest_scraped_articles()

        if not all_articles:
            raise HTTPException(status_code=404, detail="No articles to synthesize")

        # Synthesize briefing
        synthesizer = BLUFSynthesizer()
        briefing = _stamp_generated_at(await synthesizer.synthesize_region(all_articles, region))

        # Save briefing to disk
        BRIEFING_DIR.mkdir(parents=True, exist_ok=True)

        # Create filename with region and timestamp
        region_slug = region.lower().replace(' ', '_').replace('/', '_')
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        briefing_file = BRIEFING_DIR / f"{region_slug}_{timestamp}.json"

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


@app.post("/synthesize/global", dependencies=[Depends(require_admin_token)])
async def synthesize_global_briefing():
    """
    Generate a cross-regional global intelligence briefing from all scraped articles.

    Synthesizes thematic cross-regional analysis identifying connections between theaters.

    Returns:
        Generated global briefing and metadata
    """
    try:
        from synthesis.bluf_synthesizer import BLUFSynthesizer

        if not SCRAPED_DIR.exists():
            raise HTTPException(status_code=404, detail="No scraped articles found. Run /scrape first.")

        all_articles = _load_latest_scraped_articles()

        if not all_articles:
            raise HTTPException(status_code=404, detail="No articles to synthesize")

        synthesizer = BLUFSynthesizer()
        briefing = _stamp_generated_at(await synthesizer.synthesize_global(all_articles))

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
        # The host filesystem is ephemeral, so a PDF that was only sitting on disk
        # disappeared at every restart and the PDF button broke in the app while the
        # text briefings kept working from Supabase. Build the PDF from the stored
        # briefing whenever the cached file is missing or older than the briefing.
        pdf_dir = Path("data/pdfs")
        pdf_dir.mkdir(parents=True, exist_ok=True)

        region_slug = region.lower().replace(' ', '_').replace('/', '_')
        pdf_files = list(pdf_dir.glob(f"{region_slug}_*.pdf"))
        latest_pdf = max(pdf_files, key=lambda p: p.stat().st_mtime) if pdf_files else None

        briefing = await _load_briefing_for_pdf(region)

        if briefing is None and latest_pdf is None:
            raise HTTPException(status_code=404, detail=f"No PDF found for region: {region}")

        if briefing is not None and _pdf_needs_refresh(latest_pdf, briefing):
            from pdf_generation.pdf_generator_v3 import PDFGeneratorV3

            generated_path = PDFGeneratorV3().generate_pdf(briefing)
            latest_pdf = Path(generated_path)
            logger.info(f"Generated {region} PDF on demand: {latest_pdf}")

        # Inline: the web build embeds this URL in an iframe, and an attachment
        # disposition makes the browser download the file instead of rendering it,
        # which left the web PDF screen stuck on its loading spinner.
        return FileResponse(
            path=str(latest_pdf),
            media_type="application/pdf",
            headers={"Content-Disposition": f'inline; filename="{latest_pdf.name}"'},
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving PDF: {str(e)}")


@app.post("/briefing/generate-pdf", dependencies=[Depends(require_admin_token)])
async def generate_pdf(region: str = "Europe/Africa"):
    """
    Generate PDF from latest briefing JSON.

    Args:
        region: Geographic region (default: Europe/Africa)

    Returns:
        Path to generated PDF
    """
    try:
        from pdf_generation.pdf_generator_v3 import PDFGeneratorV3 as PDFGenerator

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


@app.post("/pipeline/run-weekly", dependencies=[Depends(require_admin_token)])
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
            "errors": [],
            "warnings": [],
            "storage": "supabase" if (USE_SUPABASE and supabase) else "files",
        }

        # Step 1: Scrape sources
        logger.info("Step 1: Scraping sources")
        try:
            from scrapers.orchestrator import ScraperOrchestrator
            orchestrator = ScraperOrchestrator()
            scrape_results = await orchestrator.scrape_all_sources(days=7)

            cleared_scrape_files = _clear_json_files(SCRAPED_DIR)
            orchestrator.save_all_results(scrape_results)
            summary = orchestrator.get_summary(scrape_results)
            all_articles = _flatten_scrape_results(scrape_results)

            # Log Western Hemisphere article count for debugging
            wh_count = sum(1 for a in all_articles if 'Western Hemisphere' in a.get('region_tags', []))
            logger.info(f"Western Hemisphere articles scraped: {wh_count}")

            pipeline_results["scraping"] = {
                "total_articles": summary["total_articles"],
                "by_source": summary["by_source"],
                "by_region": summary.get("by_region", {}),
                "stale_snapshots_cleared": cleared_scrape_files,
            }
            logger.info(f"Scraping complete: {summary['total_articles']} articles")
            logger.info(f"By region: {summary.get('by_region', {})}")
        except Exception as e:
            error_msg = f"Scraping failed: {str(e)}"
            logger.error(error_msg)
            pipeline_results["errors"].append(error_msg)
            return JSONResponse(status_code=500, content=pipeline_results)

        # Step 2 & 3: Synthesize briefings and generate PDFs for each region
        regional_briefings = []  # collected to compose the Global briefing
        for region in regions:
            try:
                logger.info(f"Processing region: {region}")

                # Synthesize briefing
                from synthesis.bluf_synthesizer import BLUFSynthesizer
                from pdf_generation.pdf_generator_v3 import PDFGeneratorV3 as PDFGenerator

                # Synthesize
                synthesizer = BLUFSynthesizer()
                briefing = await synthesizer.synthesize_region(all_articles, region)
                briefing['region'] = region
                # Stamp the real server time. The LLM otherwise fabricates
                # generated_at from the prompt schema, which made regional dates
                # wrong and broke Supabase's "latest" ordering (Global already
                # does this; the regional path previously did not).
                _stamp_generated_at(briefing)
                regional_briefings.append(briefing)

                # Save briefing JSON (file-based backup)
                BRIEFING_DIR.mkdir(parents=True, exist_ok=True)
                region_slug = region.lower().replace(' ', '_').replace('/', '_')
                timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
                briefing_file = BRIEFING_DIR / f"{region_slug}_{timestamp}.json"

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
                        # Surface this in the response: file storage on the host is
                        # ephemeral, so a silent caching failure means the mobile app
                        # loses every briefing at the next container restart.
                        message = f"Supabase caching failed for {region}: {e}"
                        logger.warning(message)
                        pipeline_results["warnings"].append(message)

                pipeline_results["regions_processed"].append({
                    "region": region,
                    "briefing_file": str(briefing_file),
                    "pdf_path": pdf_path,
                    "sections": len(briefing.get("sections", [])),
                    "article_count": briefing.get("article_count", 0),
                    "freshness": briefing.get("freshness", {}),
                })

                logger.info(f"Completed {region}: {len(briefing.get('sections', []))} sections")

            except Exception as e:
                error_msg = f"{region} processing failed: {str(e)}"
                logger.error(error_msg)
                pipeline_results["errors"].append(error_msg)

        # Step 4: Compose the Global briefing from the four regional briefings.
        # Global = cross-regional executive summary + every region IN FULL (no
        # fragile mega-synthesis). The exec summary is attempted via the LLM;
        # on any failure we fall back to stitching the regional BLUFs so Global
        # can never fail once the regions succeeded.
        try:
            logger.info("Step 4: Composing global briefing from regional briefings")
            from pdf_generation.pdf_generator_v3 import PDFGeneratorV3 as PDFGenerator

            if not regional_briefings:
                raise ValueError("no regional briefings available to compose Global")

            # Cross-regional executive summary (best-effort LLM; resilient fallback)
            exec_summary = ""
            global_freshness = _aggregate_freshness_blocks([
                briefing.get("freshness", {}) for briefing in regional_briefings
            ])
            try:
                from synthesis.bluf_synthesizer import BLUFSynthesizer
                gsyn = await BLUFSynthesizer().synthesize_global(all_articles)
                exec_summary = (gsyn or {}).get('bluf', '') or ''
                global_freshness = (gsyn or {}).get('freshness') or global_freshness
            except Exception as e:
                logger.warning(f"Global exec-summary synthesis failed; using regional BLUFs: {e}")
            if not exec_summary:
                exec_summary = "  ".join(
                    f"{b.get('region')}: {b.get('bluf', '')}" for b in regional_briefings
                ).strip()

            # Flatten sections (region-prefixed) so the mobile app shows the full
            # global picture; keep full sub-briefings under 'regions' for the PDF.
            flat_sections = []
            for b in regional_briefings:
                for s in b.get('sections', []):
                    flat_sections.append({
                        'title': f"{b.get('region')}: {s.get('title', '')}",
                        'content': s.get('content', ''),
                        'sources': s.get('sources', []),
                    })

            timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
            global_briefing = {
                'region': 'Global',
                'generated_at': datetime.now(timezone.utc).isoformat(),
                'bluf': exec_summary,
                'regions': regional_briefings,   # full content -> drives the PDF
                'sections': flat_sections,       # flattened -> drives the app
                'key_developments': [],
                'outlook': '',
                'article_count': sum(b.get('article_count', 0) for b in regional_briefings),
                'freshness': global_freshness,
            }

            BRIEFING_DIR.mkdir(parents=True, exist_ok=True)
            global_file = BRIEFING_DIR / f"global_{timestamp}.json"
            with open(global_file, 'w', encoding='utf-8') as f:
                json.dump(global_briefing, f, indent=2, ensure_ascii=False)

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
                "regions": len(regional_briefings),
                "sections": len(flat_sections),
                "article_count": global_briefing["article_count"],
                "freshness": global_briefing.get("freshness", {}),
            }
            logger.info(f"Global briefing complete: {len(regional_briefings)} regions, {len(flat_sections)} sections")

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


@app.get("/debug/supabase", dependencies=[Depends(require_admin_token)])
async def debug_supabase():
    """
    Test Supabase connection and show status.
    Returns connection status and sample data if available.
    """
    result = {
        "enabled": USE_SUPABASE,
        "client_initialized": supabase is not None,
        "key_role": "service_role" if (supabase and supabase.uses_service_role) else "anon",
        "briefings_count": 0,
        "sample_regions": []
    }

    if USE_SUPABASE and supabase and not supabase.uses_service_role:
        result["hint"] = (
            "Supabase is using SUPABASE_KEY (anon). Writes fail while row-level security "
            "is enabled; set SUPABASE_SERVICE_KEY on the host."
        )

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


@app.post("/debug/upload-briefing", dependencies=[Depends(require_admin_token)])
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
