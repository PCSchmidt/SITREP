# SITREP: Evidence Notes

Companion to SITREP.md. Labels: Confirmed, Ran it, Per the docs, My reading, Ask the author, Author says. Paths are relative to the repository root. Keys and tokens are named, never printed.

## E1 Fact sheet
- Name, licence: SITREP, MIT (README; mobile/LICENSE is the Expo template licence, 650 Industries). Confirmed.
- Kind: deployed backend plus phone/web app. FastAPI on Railway (Docker, Python 3.11 image), Supabase Postgres, Expo / React Native app with a web export published from a separate portfolio repo to GitHub Pages. Confirmed (Dockerfile, api/main.py, mobile/package.json, DEPLOYMENT.md).
- Commits: 123, all authored "Chris Schmidt"; first 2026-05-21, last 2026-10-07 (docs). Last code commits 2026-09-15 (eas.json, store assets) and 2026-09-12 (API, mobile). Ran it (git log).
- Size: api Python about 3,570 lines including 161 lines of tests (wc). Ran it.
- Tests: 11 (api/tests/test_admin_auth.py, test_supabase_key.py). 11 passed. Ran it (E7).
- Version: APP_VERSION 0.21.11 (api/main.py). Live service reports the same. Ran it.
- Deployed: Railway since 2026-05-26 (commit d3b7bc1 "v0.10 Production Deployment COMPLETE"); in-app daily scheduler since v0.19 (commit 52d4420, 2026-05-31); GitHub Actions backup trigger since 2026-06-04 (commit 36b10bb). Confirmed.
- Live checks, 2026-10-27, GET only against public routes: /health returned status ok, version 0.21.11, supabase_enabled true; / returned storage Supabase, scheduler "Running - Daily at 06:00 UTC", next run 2026-10-28T06:00Z; /briefing/latest for each desk and /briefing/global; the web app URL returned 200. Ran it (E15).
- Users: none evidenced. Per the docs: 15 addresses on an "Alpha tester" list; opted-in count not verified (STORE_SUBMISSION_CHECKLIST.md, PLANS.md). Ask the author.
- Cost per the docs: about $0.001 per desk briefing, about $0.15 a month for daily runs, plus Railway hosting (amount not documented). Per the docs; no billing data.
- Needs: OpenRouter key, Supabase project and service key, optional Guardian key; Playwright Chromium in the Docker image for the ISW reader.

## E2 Reading and running log
Read: README, SPEC (headings and status lists), DECISIONS (all), DEPLOYMENT (to step 8), VERSION_ROADMAP, PLANS (open work), FUTURE_VISION (head), MEMORY_CORRECTIONS, MEMORY_EPISODIC (head and last session entry), scratchnotes (head), STORE_SUBMISSION_CHECKLIST (greps), PRIVACY_POLICY (greps), .github/workflows/daily-briefing.yml, agent configuration files (head), mobile/eas.json (grep), api/main.py (guard, scheduler wiring, pipeline), api/scheduler.py, api/synthesis/openrouter_client.py, api/synthesis/bluf_synthesizer.py (all), api/scrapers/orchestrator.py, base.py, base_rss_scraper.py (region inference), database/supabase_client.py, both test files (heads), scripts/test_synthesis_comparison.py (head).
Not read: SPEC historical sections, FUTURE_VISION body, TERMS_OF_SERVICE, APP_STORE_LISTING, DESIGN_SYSTEM, CONTRACT, individual scrapers (except structure), PDF generator body, mobile source beyond hooks/analytics, the 527 committed files under mobile/api/venv (pip only), the old repository explainers (none exist per instruction).
Commands run (scratch copy via git archive; clone untouched):
- uv venv --python 3.12; uv pip install fastapi==0.115.0 httpx==0.27.2 pytest==8.3.4 pytest-asyncio==0.24.0 supabase==2.31.0 python-dotenv==1.0.1 apscheduler==3.10.4 (a subset of requirements.txt; playwright, weasyprint, lxml, aiohttp, feedparser, reportlab not installed for the test run). `pytest tests -q -p no:cacheprovider` from api/: 11 passed, 4 warnings (FastAPI on_event deprecation), 8.42 s. Ran it.
- First attempt on Python 3.14 with unpinned latest packages failed at import (pydantic-core could not load). Not the project's supported setup (README says 3.11+, Docker uses 3.11). Ran it.
- Probe script (scratch, E4) with beautifulsoup4, lxml, reportlab added unpinned.
External: public GETs to the live API and the web app only (E1). No POST, no pipeline trigger, no model call, no database access, no key used.
Final git status of the clone: clean. Confirmed.

## E3 Claims check (L1 doc matches doc, L2 re-run, L3 recomputed)
| ID | Claim (source) | Check | Verdict |
| --- | --- | --- | --- |
| CL-01 | 11 backend tests pass offline (README, DEPLOYMENT) | L2, 11 passed | supported |
| CL-02 | Thirteen scrapers by default, 14 with Guardian key (README) | orchestrator.py lists 13 and appends Guardian if key set | supported (L1) |
| CL-03 | 60 s per-attempt timeout, two retries (README) | orchestrator.py SCRAPER_TIMEOUT 60, max_retries 2; GDELT has its own longer timeout | supported, with exception |
| CL-04 | One synthesis pass per desk, then Global "stitches" (README) | pipeline also calls synthesize_global, a fifth model call, for the Global summary; Global sections are copied from the desks | partly |
| CL-05 | Every claim in a section carries the URL it came from (README) | live data: 77 of 98 sources had a url; the prompt asks the model to emit urls, and back-fill covers only exact title matches; no check that a url is real | partly (my reading; live data Ran it) |
| CL-06 | Model waterfall V4 Flash, V3.2, Kimi K2.5; model_used recorded (README) | openrouter_client.py; live desks show model_used | supported (L2 for the record, live) |
| CL-07 | A second request while a run is in progress is refused (DEPLOYMENT) | grep of api for lock, "in progress", "already running" found nothing relevant in main.py | contradicted (my reading of the code) |
| CL-08 | Briefings are in Supabase, PDFs rebuilt on demand (README, DEC-010/012) | supabase_client.py, main.py; live service says storage Supabase | supported |
| CL-09 | Docs describe SITREP_ADMIN_TOKEN as an optional setting (DEPLOYMENT, DEC-013) | live state not verified or tested; the guide makes no claim about it | per the docs; unverified |
| CL-10 | About $0.001 per desk briefing (README, DEC-009) | live token counts 9,018 to 22,109 per briefing; prices in a code comment ($0.10 and $0.20 per million tokens for V4 Flash) | plausible, not billed (L3 arithmetic only) |
| CL-11 | Last verified run 2026-09-12, 30 articles per desk, 120 for Global, 17 sections (README) | stale: live run 2026-10-27 had Global 90 articles, 14 sections | out of date |
| CL-12 | Global briefing carries BLUF, key developments, outlook (README overview) | live Global has 0 key developments; pipeline sets key_developments [] and outlook "" | contradicted |
| CL-13 | "The web app rendered every desk tab and PDF" (README) | web app returned 200; rendering not checked | unchecked |
| CL-14 | Play closed test "status and opted-in count need confirmation" (README) | consistent across docs; nothing to check | per the docs |
| CL-15 | "Sources are real and cited" (app footer copy, mobile DisclaimerBanner) | nothing verifies a cited title exists | stronger than the code checks (my reading) |
Count: 15 examined; 3 contradicted or out of date (CL-07, CL-11, CL-12), 3 partly, 6 supported, 3 unchecked or per the docs.

## E4 Rule attacks
Probe script (scratch only, not in the clone) used a fake model client that returns fixed text, calling BLUFSynthesizer directly.
- Empty article list for a desk: returns placeholder "No recent intelligence available for Middle East." Ran it.
- Fenced JSON with region "Europe" for a Middle East request: parsed; region forced to "Middle East"; a source with a title differing only in case and spacing got url restored; a plain-string source was skipped without error. Temperature passed to the client: 0.7. Ran it.
- Non-JSON reply ("Sorry, I cannot"): JSONDecodeError raised (desk fails). Ran it.
- Model returns None: a TypeError raised in the error logging path (slicing None) rather than a clean parse error. Minor defect, still a failure of that desk. Ran it.
- Fabricated citation title with no matching article: kept, no url added, no flag. Ran it.
- Region inference (RSSBaseScraper._infer_regions, titles only): "Coast Guard seizes cutter" -> Western Hemisphere (substring "oas"); "Miranda rights case" -> Middle East ("iran"); "Border security bill in Congress" -> Western Hemisphere; "Ukrainian drones hit refinery" -> Global (keyword "ukraine" is not a substring of "ukrainian"); "Tokyo markets rise (Japan)" -> Indo-Pacific; "Quiet day in sports" -> Global. Ran it.
Not attacked: the admin token with a real request (would need a POST to the live service); the pipeline lock (no code); PDF generation; prompt injection through article text; scraping.

## E5 Code map
- api/main.py: FastAPI app, admin-token dependency, startup scheduler, routes (/, /health, /scrape, /synthesize, /briefing/latest, /briefing/global, /synthesize/global, /briefing/latest/pdf, /briefing/generate-pdf, /pipeline/run-weekly, /debug/supabase, /debug/upload-briefing), pipeline orchestration (lines ~629-850).
- api/scheduler.py: APScheduler cron 06:00 UTC posting to the pipeline route.
- api/scrapers: orchestrator (13 or 14 readers, retries), base classes, RSS base and subclasses for named outlets, rss_scraper (feed bundle, several via Google News search proxies), gdelt_scraper, isw_scraper (Playwright), gov_scraper, guardian_api_scraper, latam_backup_scraper.
- api/synthesis: openrouter_client (waterfall), bluf_synthesizer (prompts, selection, parsing, back-fill, freshness diagnostics).
- api/database/supabase_client.py: one row per desk, update-or-insert.
- api/pdf_generation/pdf_generator_v3.py: reportlab layout with embedded fonts.
- api/tests: two files, 11 tests. api/scripts: ad-hoc smoke scripts (not tests; pytest collection of them errors, per README).
- mobile: Expo Router app (index, detail, pdf, about, privacy, terms), hooks/useBriefings.ts (TanStack Query), services/analytics.ts (Sentry, Mixpanel), eas.json, store-assets.
- .github/workflows/daily-briefing.yml: the only workflow. agent configuration folder.
- Oddities: mobile/api/venv (527 tracked files, a pip-only virtualenv); document_pdf.pdf (the inspiration newsletter) tracked; api/isw_debug.html tracked.

## E6 Model call sites
| Where | Model | Purpose | Settings |
| --- | --- | --- | --- |
| synthesize_region | waterfall deepseek/deepseek-v4-flash, deepseek/deepseek-v3.2, moonshotai/kimi-k2.5 via OpenRouter | write one desk briefing as JSON | temperature 0.7, max_tokens 12,000, up to 30 articles (2,000 chars each) |
| synthesize_global | same waterfall | Global summary (only the bluf field is used) | temperature 0.7, max_tokens 16,000, up to 12 per desk plus 8 untagged (2,500 chars each) |
Client: httpx timeout 120 s per call; any exception moves to the next model; empty content counts as failure; no retry within a model; no per-run or daily budget; metadata records model_used, token counts and a fixed cost string. Prices in code comments: V4 Flash $0.10/$0.20, V3.2 $0.25/$0.38, Kimi K2.5 $0.40/$1.90 per million tokens (input/output). Confirmed.
Model comparison scripts (api/scripts/test_synthesis_comparison.py, test_deepseek_kimi.py, test_moonshot_models.py) check that models answer and count tokens; no quality scoring. Confirmed (head of the first; greps of the others).
Prompts: SYSTEM_PROMPT (desk) and GLOBAL_SYSTEM_PROMPT in bluf_synthesizer.py; the desk prompt contains a full example BLUF with specific numbers and says to "EXCEED this quality standard". No prompt tests. Confirmed.
Other model-like components: none (no embeddings, no classifier).

## E7 Tests and CI
Tests: 11. test_admin_auth.py (parametrised guard cases; a test that guarded routes are exactly the mutating ones). test_supabase_key.py (stubbed supabase package; service key preferred, anon fallback, blank service key falls back, missing credentials raise). Spot checks: (1) the guard test asserts allowed or status code for header/env combinations, real behaviour of the dependency; (2) the route test inspects the app's routes for the dependency, which checks wiring, not behaviour; (3) key tests assert which key the client was created with, using a fake package, so they test selection logic only. Coverage not measured. No tests for scrapers, synthesis, PDF, database writes, mobile.
CI: no test workflow. daily-briefing.yml runs on a cron and manual dispatch: reads /briefing/global, and POSTs the pipeline route if generated_at is not today; fails if the response status is not "success". It is a production job. Any push to main redeploys Railway (README). Confirmed.

## E8 Plan-versus-results and history
No pre-registered plan or results; not applicable. History by month: May 81, June 15, August 9 (freshness PR #1 merged 2026-08-06), September 17 (14 on 2026-09-12 for outage recovery, guard, PDFs, docs; 3 on 2026-09-15 for the store), October 1. Ran it (git log).
Co-author credits: commit messages are not a reliable count of agent use; the guide says only that AI coding agents wrote almost all of the code under my direction. Confirmed.
Tool evidence: agent configuration files and instruction files are present in the repository. The guide names no tools, only "AI coding agents". My reading.
Author context says: nearly all code written by AI coding agents under the author's direction.

## E9 Gates and approvals
DECISIONS.md: 15 entries, each "Approved by: Chris Schmidt", "Owner: Chris Schmidt"; the file says it is a solo project. VERSION_ROADMAP gates have estimated and actual hours "as recorded". Nothing independent approved anything. Entries DEC-002, 003, 005 are marked NOT ADOPTED (template choices for libraries the project never used); DEC-001 and DEC-004 carry notes on what the code does. Confirmed.

## E10 Environment
requirements.txt pins fastapi 0.115.0, uvicorn 0.32.0, supabase 2.31.0, python-dotenv 1.0.1, playwright 1.48.0, beautifulsoup4 4.12.3, lxml 5.3.0, feedparser 6.0.11, weasyprint 62.3, reportlab 4.2.5, httpx 0.27.2, aiohttp 3.11.2, apscheduler 3.10.4, pytest and plugins. weasyprint has no import in api (grep); the project's notes say it failed on Windows and was replaced by reportlab: an unused pinned dependency. feedparser is declared and used by rss_scraper. Results do not record library versions except the pins. No lockfile for Python; mobile has package-lock.json. Python 3.11+ stated; Docker 3.11-slim. Ran it / Confirmed.

## E11 Security and privacy scan
- Tracked env files: .env.example, api/.env.example, mobile/.env.example only; no .env ever added in history (git log --diff-filter=A names). Confirmed. No .env was opened.
- Pattern scan of tracked files (OpenRouter-style, Supabase secret-style, JWT-like, AWS, GitHub token patterns): only a placeholder in api/SETUP_OPENROUTER.md and base64 blobs in api/isw_debug.html and package-lock.json (not keys). History scan was limited to added env files, not a full secret scan. Ran it.
- mobile/eas.json (commits touching EAS config, e.g. 8be5dbf, 2026-05-30) commits the names EXPO_PUBLIC_MIXPANEL_TOKEN and EXPO_PUBLIC_SENTRY_DSN with values in three build profiles. These are client-side analytics identifiers designed to ship inside the app, but they are in a public repo. Not printed here. Confirmed.
- Open surface: CORS allows all origins with credentials (api/main.py); the admin guard is opt-in and its live state is unverified. Admin token comparison uses secrets.compare_digest. Confirmed.
- Scraping: browser-like User-Agent string in base_rss_scraper; README says robots.txt is not consulted and no politeness delay; several outlets are reached through Google News search feeds because direct feeds returned 401/403 (code comments). Per the docs / Confirmed.
- Privacy: privacy policy says no personal data, anonymous device identifier for Mixpanel, Sentry crash reports. Per the docs.
- Note: the repository carries a third-party newsletter PDF (document_pdf.pdf). Licence of that file unknown. Ask the author.

## E12 Shortcomings register
| ID | Shortcoming | Severity | Disclosed? | Options | Recommendation |
| --- | --- | --- | --- | --- | --- |
| S1 | Nothing checks briefings against sources; citations and urls unverified | High | Yes (README "No evaluator") | A) hand-label about 50 sentences and report support rate (small); B) second-model claim check as in the author's other projects (medium); C) leave and label the app copy accurately | A then B; also soften the "sources are real" footer until measured |
| S2 | Admin guard is opt-in; live state unverified, to confirm on | High | Yes (DEC-013 known gap) | A) set SITREP_ADMIN_TOKEN on Railway and the Actions secret (small); B) rate-limit and IP-restrict (medium) | A |
| S3 | No test gate; 11 tests not run on push; any push to main redeploys | High | Not as such | A) add a pytest job on push (small); B) also add tests for readers, selection, title matching with a fake model (medium) | A first |
| S4 | Temperature 0.7 and no seed: run-to-run variation unmeasured | Medium | No | A) lower to 0 or 0.2 and compare (small); B) leave | A |
| S5 | Keyword substring region tagging misfiles articles ("oas" in "coast", "iran" in "Miranda") and misses inflections | Medium | No | A) word-boundary regex and inflections (small); B) model or classifier tagging (medium) | A, with a small hand-labelled check |
| S6 | Only the newest briefing per desk is stored; no run history; failed desk not visible to readers (Indo-Pacific stale 2026-10-27; Global composite silently lacks a desk) | Medium | Partly (README: no per-run history) | A) store dated rows and a run log table (medium); B) add a missing-desk flag to the Global record and app note (small) | B then A |
| S7 | No alerting; only a red workflow run | Medium | No | A) notify on partial failure (small); B) a health endpoint that reports freshness per desk | A |
| S8 | No spend cap on model calls | Medium | No | A) per-run token ceiling (small) | A |
| S9 | Docs ahead of code (second-run refusal, Global key developments, "one pass per desk", stale last-verified run) | Low | Partly | correct README/DEPLOYMENT | fix |
| S10 | Scraping politeness and terms (robots, browser-like identity, Google News proxy) | Medium | Yes (README limitations) | A) descriptive User-Agent and robots check (small); B) restrict to licensed or official feeds | A |
| S11 | Unused pinned weasyprint; 527 tracked pip files under mobile/api/venv; CORS "*" with credentials | Low | No | clean up | clean up |
| S12 | None content from the model causes a TypeError in the log path | Low | No | guard the slice | fix |

## E13 Math and method detail
- Selection: per desk, group by source, take newest 5 per source (sorted by source name for stability), then newest 30 overall. Global: newest 12 per desk tag plus newest 8 tagged Global.
- Region tags: lowercase title+content, substring tests against four keyword lists; no tag -> "Global". Complexity linear in articles times keywords.
- Back-fill: normalise title (collapse whitespace, lowercase), map to first article with that title, copy url, published_date, source only where missing.
- Freshness diagnostics: newest, oldest, median article age, counts within 48 hours; aggregated for Global.
- Cost arithmetic (My reading): at $0.10 in and $0.20 out per million tokens, the largest live briefing (22,109 total tokens) costs under $0.005 even if every token were output.

## E14 Discrepancies
1. README overview: Global carries key developments and outlook; code sets both empty (live: 0).
2. README: one synthesis pass per desk; code adds a fifth model call for the Global summary.
3. DEPLOYMENT and skills/deployment: a second pipeline request is refused; no locking code found.
4. README "Last verified run 2026-09-12 ... 120-article Global, 17 sections"; live 2026-10-27: 90 articles, 14 sections.
5. README: every claim carries the URL it came from; live 77 of 98 sources had one.
6. README line "Hacker-free HTML pages" is a garbled phrase; ISW is read by Playwright and others by feeds.
7. SPEC.md still carries unchecked historical items (v0.2, v0.7) marked as history.
8. DECISIONS DEC-001 rationale mentions LangGraph and SSE, which the project does not use (the entry says so).
9. API client comment says "(0-1)" temperature range; code uses 0.7 for desks and Global.

## E15 Production readiness detail
- Reality check: deployed and reachable; daily schedule since 2026-05-31; the live run on 2026-10-27 began about 06:00 and finished desks at 06:15 to 06:27 and Global at 06:28 UTC (generated_at stamps). Indo-Pacific showed generated_at 2026-10-26T06:21 UTC (written by DeepSeek V3.2, newest article 2026-10-26); Global had article_count 90 and 14 sections (ME 5 + E/A 5 + WH 4), consistent with Indo-Pacific missing from that run. Cause not visible (Railway logs and Actions history are not in the repo). My reading.
- Duration: about five months scheduled; continuity unevidenced (one row per desk, overwritten).
- Failure history, documented: 2026-06-04 missed scheduled run (workflow comment) -> backup trigger; 2026-05-31 null model content crashed Global (commit 07811d0); 2026-06-11 model-fabricated generated_at (commit febcd8a); 2026-08-06 briefing freshness selection fixes (PR #1); 2026-08-07 Western Hemisphere sources and GDELT rate limits (v0.21.5 to 7); 2026-09-12 briefing storage outage (writes with anon key failed with Postgres error 42501, briefings lived on ephemeral disk, lost on redeploy; PDFs downloaded instead of rendering). Duration of the September outage not recorded.
- Monitoring: structured response from the pipeline (per-source counts, warnings, errors); /debug/supabase; GitHub Actions failure. Phone app: Sentry crash reporting and Mixpanel events wired (services/analytics.ts); no dashboards or numbers in the repo. No alerting for partial failure.
- Rollback: none documented beyond redeploying a prior commit on Railway (not documented). Runbook: DEPLOYMENT.md steps.
- Reader numbers: none in the repository. The repository contains no record of an OpenRouter key revocation or of a failed daily run caused by one; the only model-key note is the generic 401 troubleshooting row in api/SETUP_OPENROUTER.md. Left for the questions file.
- Gap to deployable (already / partly / missing): hosting already; scheduler already; health route already; sign-in and permissions missing (no accounts by design); monitoring and alerts missing; backups missing (Supabase default unknown); rollback missing; versioned prompts partly (git only); cost limits missing; security review partly (agent definition exists, no report found); runbook partly; legal pages already.

## E16 Review dispositions
First draft; no separate review pass has run. Self-review applied: removed first-person claims about checking; replaced "links restored by the program" with the correct statement that urls may come from the model (back-fill covers only title matches); removed a claim that the 77 addresses were evidence of real articles.

## E17 Completeness and backlog
| Item | Status | Evidence |
| --- | --- | --- |
| Four regional desks plus Global | done, untested | main.py pipeline; live data |
| Thirteen readers (14 with key) | done, untested | orchestrator.py |
| Model waterfall | done, untested | openrouter_client.py; live model_used |
| Daily schedule and backup trigger | done | scheduler.py, workflow, live next_run |
| Supabase storage | done | supabase_client.py; live storage field |
| On-demand PDFs | done, untested | main.py; DEC-012 (PDF not fetched in this run) |
| Phone and web app | done, untested | mobile/; web returned 200 |
| Admin guard | opt-in (live state unverified) | DEC-013; tests |
| Play Store release | partly | PLANS.md, checklist |
| Apple App Store | planned only | PLANS.md |
| Accounts, personalisation, push, search, favourites | planned only | SPEC v1.1+ |
| Object-storage PDF archive | not built | PLANS.md |
| Evaluator or claim check | not built | README limitations |
Backlog (Finish / Fix / Improve / Add): Finish: Play closed test, then Apple. Fix: admin token on, README corrections, word-boundary regions, None-content bug. Improve: test gate in a push workflow, temperature experiment, per-desk freshness flag. Add: hand-labelled sample and a claim checker, run history table, alerting, spend cap. Milestone 1 exit test: token set (unauthenticated POST returns 401), pytest runs on push and fails on a deliberate break, 50 sentences labelled with a reported support rate.

## Diagram source
Images were drawn with matplotlib (script kept in the scratch folder, not published): SITREP-learned-vs-rules.png, SITREP-parts.png, SITREP-models.png. Chart numbers in the text come from E15 and E3.

## Revision log (2026-10-27, v1 draft to v2 revision)
Archived the prior text as SITREP.v1draft.md (6,349 words). Revised text is about 5,220 words (plain wc -w). All ten fixes from SITREP.readercheck.md applied:
1. Length cut by about a third (testing, models and parts chapters cut hardest).
2. Opening lightened; deterministic-versus-probabilistic stated in the second block, within about 200 words; hiring relevance added.
3. Vendor names (Railway, FastAPI, Supabase, Docker, Expo) moved out of "The parts" into the glossary; parts figure regenerated with plain role labels (no clipping checked). Other two figures unchanged (labels and numbers still match).
4. Glossary expanded from 6 to 27 entries (repo, README, commit, deploy, prompt, token, feed/RSS, scraping, API route, service key, admin token, fallback, and more).
5. Nine-row edge-case table turned into prose; the other two tables (production checklist, recruiter requirements) also turned into prose.
6. "Documentation runs ahead of the code" defined with an example at first mention (results chapter).
7. Prompt injection explained in one plain sentence.
8. Blueprint v11, closed test, stealth browser, rollback and robots file explained inline; "ladder of experiment" dropped.
9. Hiring line near the top; duplicated recruiter questions merged and shortened.
10. Status line now says the Indo-Pacific desk failed on the check day and the write and run routes are open. Verified: E15 (Indo-Pacific generated_at 2026-10-26, Global 90 articles and 14 sections) and E11/E12 S2, E3 CL-09 (open per docs and guard code; not tested with a live POST, so wording is "per the project's own documents").
Dropped: the fourteenth-reader detail and a few secondary examples. Production claims keep their caveats (cost unverified, usage unknown, run history not shown). No local paths or secrets in the text.

## Change log, 27 October 2026
Edited per author instructions: removed claims about the live state of the admin token (now stated as unverified, to confirm on before real use); removed tool names and the commit-hook explanation, leaving "AI coding agents" only; changed the defense-sector line to an interest statement; confirmed no secret values, key URLs or local paths in the guide or these notes. Guide is about 5,150 words.
