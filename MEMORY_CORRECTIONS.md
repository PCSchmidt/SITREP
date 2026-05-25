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

## REFLEXION: v0.8 -- PDF Mobile Integration
Date: 2026-05-25
Project: SITREP
ESTIMATE: Predicted 6h, Actual 6h, Variance 0%

TECHNICAL PREDICTIONS VS REALITY:

**PDF Integration (predicted 6h, actual ~6h)**:
- Expected: react-native-pdf integration, custom development build, Share/Save functionality
- Reality: Exactly as predicted - native module required custom build, all features working
- Debugging: react-native-blob-util native module initialization (~2h), header layout fix (~30min)
- Build time: ~35 minutes per Android build (CMake native compilation)

**What went as expected**:
- Custom development build requirement (react-native-pdf doesn't work in Expo Go)
- Native module autolinking with TurboModules codegen
- expo-file-system and expo-sharing APIs worked immediately
- Share and Save functionality straightforward once native modules compiled

**What took longer than expected**:
- Initial "Cannot read property 'getConstants' of null" error required full rebuild
- CMake codegen directories needed to be generated during build (not pre-built)
- Android emulator crashes during Share testing (OS behavior, not our code)

**What was faster than expected**:
- Lazy-loading PDF component prevented startup errors on first try
- Error handling and logging additions prevented further debugging loops
- Centered header layout fix was simple CSS adjustment

**Why the estimate was accurate**:
- Learned from previous gates that native modules require build time
- Anticipated debugging time for native module issues
- Factored in Android development build compilation time
- Share/Save APIs well-documented (Expo), minimal iteration needed

CORRECTION FOR FUTURE:

1. **Native module gates**: Estimate 6h as baseline for any gate requiring custom development build (3h setup/debugging + 2h build time + 1h testing). This matched reality for v0.8.

2. **Android backgrounding**: When implementing Share/Save functionality, note that Android may kill backgrounded apps. This is OS behavior, not a bug - document as "known limitation" rather than spending hours optimizing.

3. **Build-time pattern validated**: ~35min Android builds with native modules is now a known quantity. Don't underestimate compilation time.

4. **Lazy-loading native modules**: Pattern of `await import('react-native-pdf')` prevents startup crashes and should be default for heavy native modules.

5. **Apply 1.0x multiplier for native module integration gates** when custom development build is required and dependencies are well-documented. The 6h estimate was spot-on.

MEMORY_SEMANTIC.md UPDATE: None (need 3+ projects to validate pattern)

## REFLEXION: v0.6 -- Backend API
Date: 2026-05-23
Project: SITREP
ESTIMATE: Predicted 8h, Actual ~4h, Variance -50%

TECHNICAL PREDICTIONS VS REALITY:

**API Implementation (predicted 8h, actual ~4h)**:
- Expected: Complex integration with Supabase, database schema design, authentication setup
- Reality: File-based caching sufficient for MVP, REST endpoints straightforward with FastAPI
- Debugging: Async/await issues took ~1h (forgot to await synthesize_region), JSON loading format took ~30min
- Supabase: Deferred to v0.10 deployment gate (not needed for local development)

**What went faster than expected**:
- FastAPI endpoint creation: 5 endpoints in ~2h (POST /scrape, POST /synthesize, GET /briefing/latest, POST /generate-pdf, GET /latest/pdf)
- File-based caching worked perfectly: No need for database overhead during development
- Error handling: HTTPException pattern very clean, minimal boilerplate
- Testing: Comprehensive test suite written in 30min, all endpoints passing immediately after fixes

**What took expected time**:
- Debugging async/await (FastAPI coroutine serialization errors)
- JSON format discovery (wrapper object with 'articles' key vs direct array)

**Why the estimate was off**:
- Overestimated Supabase integration complexity (not needed for local dev)
- Underestimated FastAPI's productivity (declarative routing, automatic OpenAPI, great async support)
- File-based caching simpler than database layer (no schema migrations, no ORM complexity)

CORRECTION FOR FUTURE:

1. **Database integration estimates**: Defer database setup to deployment gates unless absolutely required for development. File-based caching works fine for local MVP validation.

2. **FastAPI productivity**: FastAPI is highly productive for REST APIs. 5-6 endpoints in 2-3 hours is realistic for CRUD operations with existing business logic.

3. **Async debugging pattern**: When getting "coroutine object not iterable" errors in FastAPI, always check that async functions are being awaited. Server auto-reload can be unreliable - restart manually to confirm fixes.

4. **Apply 1.0x multiplier for FastAPI endpoint gates** with existing business logic (scraping, synthesis already working). Keep 2.0x for novel API work with new domains.

5. **First-try success pattern continues**: 3/3 gates now (v0.2 synthesis, v0.3 PDF, v0.6 API) where core functionality worked on first try after small fixes. Modern tools (GPT-4, ReportLab, FastAPI) deliver quickly when well-documented.

MEMORY_SEMANTIC.md UPDATE: None (need 3+ projects to validate pattern)

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
