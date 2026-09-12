# FUTURE_VISION

Aspirational roadmap for closing the gap between SITREP and The LOWDOWN, the newsletter that inspired the BLUF briefing format.

> **This is an aspirational, point-in-time document.** It was written 2026-05-27 as blueprint v11 and describes the post-v1.0 vision, not the current build. Prose below keeps its 2026-05-27 framing; every roadmap item is labelled against the state verified on 2026-09-12. Do not read an unlabelled claim here as current.

## Current state (verified 2026-09-12)

| | |
| --- | --- |
| Backend | v0.21.10 (`APP_VERSION` in `api/main.py`) |
| Live API | **https://sitrep-production-6aac.up.railway.app** |
| Web app | https://pcschmidt.github.io/sitrep/ |
| Scrapers | 13 run by default, ~540 articles per run. 14 scraper files in `api/scrapers/`; `GuardianAPIScraper` runs only when `GUARDIAN_API_KEY` is set |
| Pipeline | The full job takes about 20 minutes; the internal APScheduler job runs it daily at 06:00 UTC |
| Verified on | 2026-09-12 |

---

## Purpose

SITREP was conceived as an **improvement** over The LOWDOWN newsletter (the inspiration PDF: `document_pdf.pdf`). Vision statement (2026-05-27): exceed The LOWDOWN in sources, styling, and analysis. This file documents the gaps between the v1.0 MVP and the full vision, with a roadmap for closing them in v1.1+.

---

## Baseline comparison: SITREP vs The LOWDOWN

### SITREP at v1.0 (2026-05-27 snapshot, superseded)

The SITREP column below is a 2026-05-27 snapshot, not the current build. The next table gives the state verified on 2026-09-12. This table is kept for the decision trail.

| Dimension | The LOWDOWN (May 2026) | SITREP (v1.0, 2026-05-27) | Status |
|-----------|------------------------|---------------------------|--------|
| **Sources per region** | 12-17 diverse sources | 7-8 sources (mostly ISW) | **BEHIND** |
| **Scraper coverage** | N/A (unknown tool) | 25% (1/4 working) | **INCOMPLETE** |
| **PDF pages** | 18 total (4-5 per region) | 12 total (3 per region) | **BEHIND** |
| **PDF styling** | Embedded maps, infographics, multi-column layout, hyperlinked sources | Basic text with amber borders, no images | **BEHIND** |
| **Analysis depth** | Deep subsections with numbered hierarchies, geopolitical context, strategic implications | Brief bullet points, surface-level | **BEHIND** |
| **Content freshness** | Weekly (unknown schedule) | Weekly (Railway cron) | **PARITY** |
| **Mobile delivery** | Email PDF attachment | Native app with PDF viewer | **AHEAD** |
| **Cost per briefing** | Unknown (likely GPT-4) | $0.001 (DeepSeek V4 Flash) | **AHEAD** |
| **Platform** | Email newsletter | iOS/Android app | **AHEAD** |

### SITREP today (2026-09-12)

Verified 2026-09-12 unless a row says otherwise.

| Dimension | The LOWDOWN (May 2026) | SITREP today (2026-09-12) | Status |
|-----------|------------------------|---------------------------|--------|
| **Sources per region** | 12-17 diverse sources | 30 articles per regional desk on the 2026-09-12 run | PARITY on volume |
| **Scraper coverage** | N/A (unknown tool) | 14 scraper files in `api/scrapers/`; 13 run by default, ~540 articles per run. `GuardianAPIScraper` runs only when `GUARDIAN_API_KEY` is set | RESOLVED |
| **PDF pages** | 18 total (4-5 per region) | Not re-measured in this pass | NOT MEASURED |
| **PDF styling** | Embedded maps, infographics, multi-column layout, hyperlinked sources | Executive PDF generator v3: PT Serif headlines with Lato body, two-column cover (Contents + Executive Summary), hyperlinked per-section sources | PARTIAL - no embedded maps or infographics yet |
| **Analysis depth** | Deep subsections with numbered hierarchies, geopolitical context, strategic implications | Synthesis prompts now ask for numbered subsections and strategic implications; no side-by-side quality measurement against The LOWDOWN has been run | PARTIAL |
| **Content freshness** | Weekly (unknown schedule) | Daily at 06:00 UTC | AHEAD |
| **Cross-regional synthesis** | One weekly issue | Composite Global briefing that stitches all four regional desks in full: 17 sections, 120 articles on the 2026-09-12 run | AHEAD |
| **Mobile delivery** | Email PDF attachment | Native app with PDF viewer (Expo SDK ~56, `react-native-pdf`; web uses an iframe with a 6s fallback timer) | AHEAD |
| **Cost per briefing** | Unknown (likely GPT-4) | About $0.013/day for five briefings, measured | AHEAD |
| **Platform** | Email newsletter | iOS/Android app; Google Play submission is the next gate | AHEAD |

### Key insights (2026-05-27 snapshot)

These notes describe 2026-05-27. Source diversity and typography have changed since; see the table above.

**Where we're ahead:**
- Mobile-first experience (vs email attachment)
- Cost efficiency (99% cheaper per briefing)
- App Store distribution (vs newsletter subscription)

**Where we're behind:**
- **Source diversity**: Only ISW scraper working (Defense One, Breaking Defense, IISS broken)
- **PDF quality**: No embedded maps, no infographics, basic typography
- **Analysis depth**: Shorter synthesis, less strategic context

**Status of these gaps (2026-09-12):**
- **Source diversity**: resolved. 13 scrapers run by default, ~540 articles per run.
- **PDF quality**: partly resolved. Executive PDF generator v3 covers typography, cover layout and hyperlinked sources; embedded ISW maps and infographics are still open (v1.2).
- **Analysis depth**: partly addressed. Prompts are deeper and a composite Global briefing exists, but no measured quality comparison against The LOWDOWN has been run.

---

## The vision: v1.1+ roadmap

### v1.1: source expansion wave 2 (est. 12-16h)

**Goal**: Reach 15-20 working sources. v0.11 completed the base expansion (6 sources, ~84 articles/week). Wave 2 adds regional depth — particularly Asia-Pacific, Africa, and Latin America which remain underrepresented.

**Status at the time**: v0.11 COMPLETE (2026-05-29)
- [x] Defense One, Breaking Defense: rewritten to RSS (were broken HTML scrapers)
- [x] IISS replaced with War on the Rocks (IISS is 403 Forbidden)
- [x] Added: The War Zone, Al Jazeera (topic-filtered)
- [x] RSSBaseScraper base class — zero new dependencies, fast, reliable

**Shipped since (verified 2026-09-12)**: 14 scraper files in `api/scrapers/`; 13 run by default and produce ~540 articles per run. `GuardianAPIScraper` runs only when `GUARDIAN_API_KEY` is set. The RSS-first approach planned here is what shipped: Defense One, Breaking Defense, War on the Rocks, The War Zone, Al Jazeera, Foreign Policy, CFR and The Diplomat all run over RSS.

**Still planned**: the success criteria below (15+ scrapers) is not met, because 13 run by default. These planned sources are not in `api/scrapers/` today: The Africa Report, Americas Society/AS-COA, International Crisis Group, East Asia Forum, Lowy Institute, ISS Africa, NACLA and SIPRI. Per-source article counts are not tracked per region, so the diversity scores below are targets, not measurements.

**Wave 2 tasks (all RSS-based, use RSSBaseScraper)**:

RSS confirmed working (tested 2026-05-29):
1. The Diplomat (`/feed/`, 96 items) — Asia-Pacific focus, strong Indo-Pacific depth
2. The Africa Report (`/feed/`, 10 items) — Sub-Saharan Africa political/business
3. Americas Society/AS-COA (`/rss.xml`, 10 items) — Latin America policy, economics
4. Council on Foreign Relations (`/feed`, 24 items) — multi-region expert analysis
5. International Crisis Group (`/rss.xml`, 10 items) — conflict-focused, country-level
6. Foreign Policy (`/feed/`, 25 items) — broad international, free tier

RSS likely working on Railway (DNS blocked locally, same pattern as earlier sources):
7. East Asia Forum (ANU) — Indo-Pacific economics and security
8. Lowy Institute — Australia foreign policy, South Pacific coverage
9. ISS Africa — Sub-Saharan Africa conflict and governance
10. NACLA — Latin American politics and social movements
11. SIPRI — Arms, conflict, security economics

**Success Criteria**:
- 15+ working scrapers
- Africa and Latin America have ≥20 articles/week each
- Asia-Pacific has ≥30 articles/week (currently Indo-Pacific underserved)
- Source diversity score > 8 per region

**Deferred to**: v1.1 gate (post-v1.0)

---

### v1.2: PDF enhancement - visual parity (est. 12-16h)

**Goal**: Match The LOWDOWN's visual quality (maps, infographics, multi-column layout)

**Tasks**:
1. **Embed ISW maps** (~4h)
   - Scrape ISW map images during article extraction
   - Store maps in data/maps/ directory
   - Integrate map images into PDF generation (ReportLab Image API)
   - Position maps contextually within relevant sections
2. **Multi-column layout** (~3h)
   - Migrate from single-column Paragraph flow to Frame-based layout
   - Implement 2-column body text (like The LOWDOWN)
   - Keep BLUF and headers single-column for emphasis
3. **Hyperlinked sources** (~2h)
   - Convert plain-text source citations to clickable hyperlinks
   - Add URL references to each source in bibliography
4. **Infographics** (~4h)
   - Generate simple charts/graphs for key metrics (casualties, territorial control)
   - Use matplotlib or similar to create visual data summaries
   - Embed as images in PDF
5. **Typography improvements** (~2h)
   - Add more visual hierarchy (section headers, subsection headers)
   - Improve spacing and margins
   - Add page numbers and footer branding

**Shipped since (verified 2026-09-12)**:
- [x] Hyperlinked sources (task 3) — `api/pdf_generation/pdf_generator_v3.py` links the sources of each section
- [x] Typography improvements (task 5) — PDF generator v3 uses PT Serif headlines with Lato body, a navy palette, hairline rules, running headers and footers, and numbered sections
- [x] Multi-column cover — the cover is two columns (Contents + Executive Summary). The body text is still single column, so task 2 is only partly done

**Still planned**:
- [ ] Embedded ISW maps (task 1) — the v3 generator has no map handling and there is no map-storage step
- [ ] Infographics (task 4) — no chart generation in the PDF path
- [ ] Two-column body text (the rest of task 2)

**Success criteria, corrected 2026-09-12**:
- [ ] PDF includes at least 1 ISW map per region — NOT met
- [x] Multi-column layout matching The LOWDOWN aesthetic — partly met (two-column cover only)
- [x] All sources hyperlinked and clickable — met
- [ ] File size < 20MB (with image compression) — not measured in this pass

**Deferred to**: v1.2 gate

---

### v1.3: analysis depth enhancement (est. 8-12h)

**Goal**: Exceed The LOWDOWN's analytical depth and strategic insight

**Tasks**:
1. **Richer synthesis prompts** (~3h)
   - Expand system prompt with deeper BLUF guidance
   - Add subsection structure (numbered hierarchies like The LOWDOWN)
   - Request strategic implications and outlook sections
   - Increase token budget for synthesis (from ~1000 to ~2500 completion tokens)
2. **Multi-pass synthesis** (~4h)
   - First pass: Extract key themes and developments
   - Second pass: Generate BLUF and strategic analysis
   - Third pass: Add geopolitical context and outlook
   - Cost impact: ~$0.003/briefing (still 99% cheaper than GPT-4)
3. **Cross-regional context** (~3h)
   - Add synthesis step that analyzes connections between regions
   - Generate "Global Strategic Outlook" section
   - Highlight cascading effects (e.g., Iran → Europe energy crisis)
4. **Confidence scoring** (~2h)
   - Add LLM self-assessment of confidence in key claims
   - Flag low-confidence assertions with disclaimers
   - Cite specific sources for high-impact claims

**Shipped since (verified 2026-09-12)**:
- [x] Richer synthesis prompts (task 1) - observed output was 10.6k-16.7k tokens per regional briefing on the 2026-09-12 run — `api/synthesis/bluf_synthesizer.py` asks for numbered subsections, strategic implications and an outlook
- [x] Cross-regional context (task 3) — a composite Global briefing now stitches all four regional desks in full: 17 sections and 120 articles on the 2026-09-12 run

**Still planned**:
- [ ] Multi-pass synthesis (task 2) — one synthesis call per briefing runs today; there is no three-pass pipeline in `api/synthesis/`
- [ ] Confidence scoring (task 4) — the synthesizer has no confidence field and no low-confidence flag. The model waterfall is deepseek-v4-flash, then deepseek-v3.2, then kimi-k2.5; empty or rate-limited responses fall through

**Success criteria, corrected 2026-09-12**:
- [ ] Average PDF length 15-20 pages — not re-measured in this pass
- [ ] BLUF quality score > 8/10 — subjective, and no user survey has been run
- [ ] Strategic outlook section present in all briefings — not verified in this pass
- [x] Cross-regional connections identified — met: the composite Global briefing covers all four desks

**Deferred to**: v1.3 gate

---

### v1.4: advanced features (est. 16-24h)

**Goal**: Features that The LOWDOWN doesn't have (mobile advantage)

**Shipped since (verified 2026-09-12)**: none of these shipped. `mobile/package.json` has no `expo-notifications`, no SQLite dependency and no Supabase Auth. `expo-sharing` is installed, but the app shares the whole PDF, not individual BLUF sections.

**Tasks** (all still planned):
1. **Push notifications** (~4h)
   - Integrate expo-notifications
   - Send push when new briefing is ready
   - User preference: notify on publish or manual refresh only
2. **Personalized region preferences** (~3h)
   - User can prioritize specific regions
   - Briefing order reflects user preferences
   - Analytics track which regions users read most
3. **Search/filter past briefings** (~6h)
   - Local SQLite database for briefing history
   - Search by keyword, date, region
   - Bookmark specific articles or sections
4. **Share specific sections** (~3h)
   - Share individual BLUF sections (not just whole PDF)
   - Generate social media cards with key quotes
   - Email sharing with formatted excerpts
5. **Supabase Auth** (~4h)
   - User accounts for cross-device sync
   - Save bookmarks and preferences to cloud
   - Optional: premium tier for priority notifications

**Success criteria (targets; none met on 2026-09-12)**:
- [ ] Push notifications working on iOS and Android
- [ ] User preferences persist across sessions
- [ ] Search returns results in < 500ms

**Deferred to**: v1.4+ gates

---

## Cost model: v1.1+ projections

Every figure in this section is a 2026-05-27 projection unless it is marked measured. Nothing here was re-measured on 2026-09-12 except the one measured line below.

**Measured cost today (2026-09-12)**: about $0.013/day for five briefings (four regional desks plus the composite Global). The stated per-briefing model rates are $0.001 for deepseek-v4-flash, $0.003 for deepseek-v3.2 and $0.009 for kimi-k2.5.

### Source expansion impact (v1.1)

**Assumed baseline (v1.0)**:
- 1 scraper (ISW): ~16 articles/week/region
- LLM input: ~7,000 tokens
- Cost: $0.001/briefing

**Projected after v1.1**:
- 12 scrapers: ~30-50 articles/week/region
- LLM input: ~15,000 tokens
- Cost: $0.002/briefing (still about 99% cheaper than GPT-4)

### PDF enhancement impact (v1.2)

**Image hosting**:
- ISW maps: ~4 images/region (16 total)
- File size: ~5MB total (compressed)
- Railway bandwidth: negligible (~20MB/week)

**Cost**: $0/month (within Railway free tier bandwidth)

### Analysis depth impact (v1.3)

**Multi-pass synthesis**:
- 3 LLM passes instead of 1
- Total tokens: ~25,000 input + ~2,500 output
- Cost: $0.003/briefing (3x current, still 99% cheaper)

**Monthly cost projection (2026-05-27)**:
- 4 briefings/month × $0.003 = **$0.012/month**
- Total: **< $1/month** (well under $20 ceiling)

**Caveat (2026-09-12)**: the monthly figure assumes a weekly cadence. The pipeline now runs daily and produces five briefings, so $0.012/month understates the current total. The measured figure is about $0.013/day.

---

## Competition tracking

### The LOWDOWN (baseline)

- **Publisher**: 157th Ops Support Squadron (military unit)
- **Frequency**: Weekly (unknown day)
- **Format**: Email PDF attachment
- **Sources**: ~12-17 per region (ISW, Defense One, Breaking Defense, IISS, Foreign Policy, CSIS, Al Jazeera, BBC, CNN, NYT, etc.)
- **Coverage**: Middle East, Indo-Pacific, Europe/Africa, Western Hemisphere
- **Cost**: Unknown (likely GPT-4, high cost per briefing)
- **Distribution**: Email subscription (unknown subscriber count)

### Other competitors

- **Morning Brief (The War Zone)**: Daily email, military aviation focus, free
- **The D Brief (Defense One)**: Daily email, Pentagon insider news, free
- **ISW Daily Updates**: Daily web posts, Ukraine/Russia focus, free
- **CSIS Commentary**: Ad-hoc analysis, policy focus, free

**SITREP's unique value prop** (2026-05-27 wording):
- Only mobile-first OSINT briefing app
- Cost-optimized for personal use ($5-6/month vs $50+ for newsletter subscriptions)

The $5-6/month figure is a 2026-05-27 estimate of total running cost. The measured LLM-only cost on 2026-09-12 is about $0.013/day.
- Cross-regional synthesis (not single-region like ISW)
- Portfolio showcase quality (not just functional)

---

## Risks & mitigation

### Risk 1: source paywalls

**Risk**: Premium sources (Jane's, Foreign Policy subscriptions) require CloakBrowser or paid access.

**Mitigation**:
- Start with free sources (ISW, Defense One, Breaking Defense, IISS, CSIS, Reuters, Al Jazeera, BBC)
- Add CloakBrowser only if free sources insufficient
- Budget $10-20/month for CloakBrowser if needed

### Risk 2: PDF generation complexity

**Risk**: Embedding maps and multi-column layout may be complex with ReportLab.

**Mitigation**:
- ReportLab supports images (Image API) and frames (Frame API)
- If ReportLab becomes limiting, consider WeasyPrint (HTML→PDF) as alternative
- Keep existing ReportLab code for fallback

### Risk 3: LLM quality degradation

**Risk**: Longer prompts and multi-pass synthesis may reduce output quality.

**Mitigation**:
- Test iteratively: compare single-pass vs multi-pass output
- Use DeepSeek V3.2 as fallback if V4 Flash quality drops
- Keep Kimi K2.5 as final fallback

### Risk 4: mobile app complexity

**Risk**: Advanced features (push notifications, search, auth) may introduce bugs.

**Mitigation**:
- Defer to v1.4+ (after v1.0 is stable and deployed)
- Test each feature in isolation before integration
- Use feature flags to toggle new features on/off

---

## Success metrics

These are targets for the v1.1-v1.4 gates, not results. The 2026-09-12 status of each gate is in the roadmap sections above.

### v1.1 (source parity)
- [ ] All 4 Tier 1 scrapers working
- [ ] 30+ articles per region per week
- [ ] Source diversity score > 10 per region

Status 2026-09-12: 13 scrapers run by default; per-region and per-source counts are not tracked, so these targets are unmeasured.

### v1.2 (PDF enhancement)
- [ ] PDF includes ISW maps
- [ ] Multi-column layout implemented
- [ ] All sources hyperlinked
- [ ] User feedback score > 8/10 on PDF quality

Status 2026-09-12: hyperlinked sources met; two-column cover shipped, two-column body still open; ISW maps not shipped; no user feedback survey has been run.

### v1.3 (analysis depth)
- [ ] Average PDF length 15-20 pages
- [ ] Strategic outlook section present
- [ ] Cross-regional connections identified
- [ ] User feedback score > 8/10 on analysis quality

Status 2026-09-12: composite Global briefing met; page length and the outlook section are not verified; no user feedback survey has been run.

### v1.4 (advanced features)
- [ ] Push notifications working
- [ ] User preferences persist
- [ ] Search returns results in < 500ms
- [ ] User retention > 70% (weekly active)

Status 2026-09-12: none of these shipped; see the v1.4 section above.

---

## Timeline estimate

This is a 2026-05-27 estimate, not a commitment. Assuming 10-15h/week:

- **v1.1 (Source Parity)**: 1-2 weeks
- **v1.2 (PDF Enhancement)**: 2-3 weeks
- **v1.3 (Analysis Depth)**: 1-2 weeks
- **v1.4 (Advanced Features)**: 2-4 weeks

**Total: 6-11 weeks (~2-3 months post-v1.0)**

---

## Decision log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-05-27 | Created FUTURE_VISION.md | Track "exceed The LOWDOWN" goals for v1.1+ |
| 2026-05-27 | Defer source expansion to v1.1 | v1.0 MVP ships with ISW alone, fix scrapers post-launch |
| 2026-05-27 | Defer PDF enhancement to v1.2 | ReportLab basic styling sufficient for v1.0 portfolio |
| 2026-05-27 | Defer advanced features to v1.4 | Focus on core briefing quality before adding bells/whistles |
| 2026-09-12 | Review FUTURE_VISION.md against the shipped build (v0.21.10) | Label shipped items against planned ones; no new commitments made |

---

## Notes

- This roadmap is aspirational, not committed. v1.0 is the portfolio-ready milestone.
- Features beyond v1.0 depend on user feedback and personal bandwidth.
- Cost ceiling remains $20/month even with all enhancements.
- The LOWDOWN serves as a quality benchmark, not a direct competitor (we're mobile-first, they're email).
- Roadmap status in this file was reviewed and labelled on 2026-09-12 against `api/scrapers/` and `api/pdf_generation/pdf_generator_v3.py`.

---

## Related docs

- [README.md](README.md) - what SITREP is and how to run it
- [SPEC.md](SPEC.md) - current architecture and API surface
- [VERSION_ROADMAP.md](VERSION_ROADMAP.md) - release history and shipped version plan
- [PLANS.md](PLANS.md) - open work items
