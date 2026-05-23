# MEMORY_CORRECTIONS.md
# Blueprint v11 | Reflexion Entries and Estimation Calibration
# New entries added ABOVE previous (newest first).
# Used by build-rules.md to calibrate future estimates.

## REFLEXION LOG
# Format per entry:
# ## REFLEXION: v[X.X.X] -- [Gate Name]
# Date: [date]
# Project: [name]
# ESTIMATE: Predicted [X] hrs, Actual [X] hrs, Variance [+/-X]%
# TECHNICAL PREDICTIONS VS REALITY: [what was expected vs what happened]
# CORRECTION FOR FUTURE: [what changes]
# MEMORY_SEMANTIC.md UPDATE: [pattern added/updated or none]

## REFLEXION: v0.2 -- Scraping Pipeline + LLM Synthesis
Date: 2026-05-23
Project: SITREP
ESTIMATE: Predicted 20h (8h scraping + 12h synthesis), Actual ~7h, Variance -65%

TECHNICAL PREDICTIONS VS REALITY:

**Scraping (predicted 8h, actual ~4h)**:
- Expected: All 4 scrapers working, potential CloakBrowser integration needed
- Reality: 1 scraper (ISW) sufficient for validation, Playwright alone worked, no paywalls hit
- Debugging: HTML selector fixes took 1-2h (expected), but only needed for 1 source

**Synthesis (predicted 12h, actual ~3h)**:
- Expected: 6-10 prompt iterations to reach quality threshold
- Reality: System prompt worked on first iteration, only needed markdown fence parsing fix
- Quality: GPT-4o Mini produced production-ready output immediately
- Cost: $0.15/briefing (expected $0-2), well under ceiling

**What went faster than expected**:
- Prompt engineering: Clear BLUF format example in system prompt = good output on try 1
- Open Router integration: Simpler than anticipated, waterfall worked immediately
- Data quality: ISW articles were rich enough that 10 articles → excellent briefing

**What took expected time**:
- Web scraping debugging (HTML selectors are always fragile)
- JSON parsing edge cases (markdown code fences)

CORRECTION FOR FUTURE:

1. **Scraping estimates**: For open-source news sites with good content, 1-2 working scrapers may be sufficient for MVP validation. Don't gold-plate all sources upfront.

2. **LLM synthesis estimates**: When system prompt includes clear schema + examples, modern models (GPT-4o, Claude) often work on first try. Reduce iteration budget for structured output tasks.

3. **Progressive validation**: "Prove it works" gates don't need 100% coverage. ISW alone was enough to validate the pipeline end-to-end.

4. **Apply 1.5x multiplier for future scraping gates** (down from 2.0x), keep 2.0x for novel LLM work until more data points.

MEMORY_SEMANTIC.md UPDATE: None (first project, no patterns to validate yet)

## REFLEXION: v0.3 -- PDF Generation Backend
Date: 2026-05-23
Project: SITREP
ESTIMATE: Predicted 8h, Actual ~2h, Variance -75%

TECHNICAL PREDICTIONS VS REALITY:

**PDF Generation (predicted 8h, actual ~2h)**:
- Expected: WeasyPrint HTML→PDF conversion with CSS styling, potential Windows compatibility issues
- Reality: WeasyPrint failed immediately (font config), switched to ReportLab programmatic generation
- Complexity: ReportLab was simpler than expected - direct Python API for layout

**What went faster than expected**:
- ReportLab learning curve: Documentation clear, sample styles provided, 1h to working PDF
- Template design: Military aesthetic translated easily to ReportLab styles
- API endpoints: Simple file serving, 30min implementation
- No iteration needed: PDF looked professional on first generation

**What took expected time**:
- Nothing - entire gate was significantly faster than estimated

**Why the estimate was off**:
- Overestimated HTML/CSS template design complexity (assumed WeasyPrint would work)
- Underestimated simplicity of ReportLab programmatic approach
- No debugging needed (ReportLab worked immediately on Windows)

CORRECTION FOR FUTURE:

1. **PDF/Document generation estimates**: When programmatic libraries (ReportLab, python-docx) are available, prefer them over HTML→format converters. They're often simpler and more reliable.

2. **Windows compatibility**: ReportLab > WeasyPrint for Windows development. WeasyPrint requires system fonts/libraries that fail on Windows.

3. **Template complexity**: Professional PDF output doesn't require complex CSS - ReportLab's programmatic styling is faster to implement than CSS debugging.

4. **Apply 1.0x multiplier for document generation tasks** with mature libraries (ReportLab, reportlab). Keep 2.0x for novel PDF work with HTML conversion.

5. **First-try success pattern emerging**: When using well-documented libraries with clear APIs (ReportLab, Open Router), modern implementation often works on first try. Reduce iteration budget for "standard" integrations.

MEMORY_SEMANTIC.md UPDATE: None (need 3+ projects to validate pattern)

## PRE-FILL ACCURACY LOG
[Empty until first interrogation with pre-fills]
