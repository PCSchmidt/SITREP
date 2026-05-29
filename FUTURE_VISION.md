# FUTURE_VISION.md
# Blueprint v11 | Post-v1.0 Enhancement Roadmap
# Vision: Exceed The LOWDOWN in sources, styling, and analysis

---

## PURPOSE

SITREP was conceived as an **improvement** over The LOWDOWN newsletter (the inspiration PDF: `document_pdf.pdf`). This file documents the gaps between our current v1.0 MVP and the full vision, with a roadmap for closing them in v1.1+.

---

## BASELINE COMPARISON: SITREP vs The LOWDOWN

### Current State (v1.0 MVP)

| Dimension | The LOWDOWN (May 2026) | SITREP (v1.0) | Status |
|-----------|------------------------|---------------|--------|
| **Sources per region** | 12-17 diverse sources | 7-8 sources (mostly ISW) | ❌ **BEHIND** |
| **Scraper coverage** | N/A (unknown tool) | 25% (1/4 working) | ❌ **INCOMPLETE** |
| **PDF pages** | 18 total (4-5 per region) | 12 total (3 per region) | ❌ **BEHIND** |
| **PDF styling** | Embedded maps, infographics, multi-column layout, hyperlinked sources | Basic text with amber borders, no images | ❌ **BEHIND** |
| **Analysis depth** | Deep subsections with numbered hierarchies, geopolitical context, strategic implications | Brief bullet points, surface-level | ❌ **BEHIND** |
| **Content freshness** | Weekly (unknown schedule) | Weekly (Railway cron) | ✅ **PARITY** |
| **Mobile delivery** | Email PDF attachment | Native app with PDF viewer | ✅ **AHEAD** |
| **Cost per briefing** | Unknown (likely GPT-4) | $0.001 (DeepSeek V4 Flash) | ✅ **AHEAD** |
| **Platform** | Email newsletter | iOS/Android app | ✅ **AHEAD** |

### Key Insights

**Where we're ahead:**
- Mobile-first experience (vs email attachment)
- Cost efficiency (99% cheaper per briefing)
- App Store distribution (vs newsletter subscription)

**Where we're behind:**
- **Source diversity**: Only ISW scraper working (Defense One, Breaking Defense, IISS broken)
- **PDF quality**: No embedded maps, no infographics, basic typography
- **Analysis depth**: Shorter synthesis, less strategic context

---

## THE VISION: v1.1+ ROADMAP

### v1.1: Source Expansion Wave 2 (Est: 12-16h)

**Goal**: Reach 15-20 working sources. v0.11 completed the base expansion (6 sources, ~84 articles/week). Wave 2 adds regional depth — particularly Asia-Pacific, Africa, and Latin America which remain underrepresented.

**Status**: v0.11 COMPLETE (2026-05-29)
- ✅ Defense One, Breaking Defense: rewritten to RSS (were broken HTML scrapers)
- ✅ IISS replaced with War on the Rocks (IISS is 403 Forbidden)
- ✅ Added: The War Zone, Al Jazeera (topic-filtered)
- ✅ RSSBaseScraper base class — zero new dependencies, fast, reliable

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

### v1.2: PDF Enhancement - Visual Parity (Est: 12-16h)

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

**Success Criteria**:
- ✅ PDF includes at least 1 ISW map per region
- ✅ Multi-column layout matching The LOWDOWN aesthetic
- ✅ All sources hyperlinked and clickable
- ✅ File size < 20MB (with image compression)

**Deferred to**: v1.2 gate

---

### v1.3: Analysis Depth Enhancement (Est: 8-12h)

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

**Success Criteria**:
- ✅ Average PDF length 15-20 pages (up from 12)
- ✅ BLUF quality score > 8/10 (subjective, user feedback)
- ✅ Strategic outlook section present in all briefings
- ✅ Cross-regional connections identified

**Deferred to**: v1.3 gate

---

### v1.4: Advanced Features (Est: 16-24h)

**Goal**: Features that The LOWDOWN doesn't have (mobile advantage)

**Tasks**:
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

**Success Criteria**:
- ✅ Push notifications working on iOS and Android
- ✅ User preferences persist across sessions
- ✅ Search returns results in < 500ms

**Deferred to**: v1.4+ gates

---

## COST MODEL: v1.1+ Projections

### Source Expansion Impact (v1.1)

**Current (v1.0)**:
- 1 scraper (ISW): ~16 articles/week/region
- LLM input: ~7,000 tokens
- Cost: $0.001/briefing

**After v1.1**:
- 12 scrapers: ~30-50 articles/week/region
- LLM input: ~15,000 tokens
- Cost: $0.002/briefing (still 99% cheaper than GPT-4)

### PDF Enhancement Impact (v1.2)

**Image hosting**:
- ISW maps: ~4 images/region (16 total)
- File size: ~5MB total (compressed)
- Railway bandwidth: negligible (~20MB/week)

**Cost**: $0/month (within Railway free tier bandwidth)

### Analysis Depth Impact (v1.3)

**Multi-pass synthesis**:
- 3 LLM passes instead of 1
- Total tokens: ~25,000 input + ~2,500 output
- Cost: $0.003/briefing (3x current, still 99% cheaper)

**Monthly cost projection**:
- 4 briefings/month × $0.003 = **$0.012/month**
- Total: **< $1/month** (well under $20 ceiling)

---

## COMPETITION TRACKING

### The LOWDOWN (Baseline)

- **Publisher**: 157th Ops Support Squadron (military unit)
- **Frequency**: Weekly (unknown day)
- **Format**: Email PDF attachment
- **Sources**: ~12-17 per region (ISW, Defense One, Breaking Defense, IISS, Foreign Policy, CSIS, Al Jazeera, BBC, CNN, NYT, etc.)
- **Coverage**: Middle East, Indo-Pacific, Europe/Africa, Western Hemisphere
- **Cost**: Unknown (likely GPT-4, high cost per briefing)
- **Distribution**: Email subscription (unknown subscriber count)

### Other Competitors

- **Morning Brief (The War Zone)**: Daily email, military aviation focus, free
- **The D Brief (Defense One)**: Daily email, Pentagon insider news, free
- **ISW Daily Updates**: Daily web posts, Ukraine/Russia focus, free
- **CSIS Commentary**: Ad-hoc analysis, policy focus, free

**SITREP's unique value prop**:
- Only mobile-first OSINT briefing app
- Cost-optimized for personal use ($5-6/month vs $50+ for newsletter subscriptions)
- Cross-regional synthesis (not single-region like ISW)
- Portfolio showcase quality (not just functional)

---

## RISKS & MITIGATION

### Risk 1: Source Paywalls

**Risk**: Premium sources (Jane's, Foreign Policy subscriptions) require CloakBrowser or paid access.

**Mitigation**:
- Start with free sources (ISW, Defense One, Breaking Defense, IISS, CSIS, Reuters, Al Jazeera, BBC)
- Add CloakBrowser only if free sources insufficient
- Budget $10-20/month for CloakBrowser if needed

### Risk 2: PDF Generation Complexity

**Risk**: Embedding maps and multi-column layout may be complex with ReportLab.

**Mitigation**:
- ReportLab supports images (Image API) and frames (Frame API)
- If ReportLab becomes limiting, consider WeasyPrint (HTML→PDF) as alternative
- Keep existing ReportLab code for fallback

### Risk 3: LLM Quality Degradation

**Risk**: Longer prompts and multi-pass synthesis may reduce output quality.

**Mitigation**:
- Test iteratively: compare single-pass vs multi-pass output
- Use DeepSeek V3.2 as fallback if V4 Flash quality drops
- Keep Kimi K2.5 as final fallback

### Risk 4: Mobile App Complexity

**Risk**: Advanced features (push notifications, search, auth) may introduce bugs.

**Mitigation**:
- Defer to v1.4+ (after v1.0 is stable and deployed)
- Test each feature in isolation before integration
- Use feature flags to toggle new features on/off

---

## SUCCESS METRICS

### v1.1 (Source Parity)
- [ ] All 4 Tier 1 scrapers working
- [ ] 30+ articles per region per week
- [ ] Source diversity score > 10 per region

### v1.2 (PDF Enhancement)
- [ ] PDF includes ISW maps
- [ ] Multi-column layout implemented
- [ ] All sources hyperlinked
- [ ] User feedback score > 8/10 on PDF quality

### v1.3 (Analysis Depth)
- [ ] Average PDF length 15-20 pages
- [ ] Strategic outlook section present
- [ ] Cross-regional connections identified
- [ ] User feedback score > 8/10 on analysis quality

### v1.4 (Advanced Features)
- [ ] Push notifications working
- [ ] User preferences persist
- [ ] Search returns results in < 500ms
- [ ] User retention > 70% (weekly active)

---

## TIMELINE ESTIMATE

Assuming 10-15h/week:

- **v1.1 (Source Parity)**: 1-2 weeks
- **v1.2 (PDF Enhancement)**: 2-3 weeks
- **v1.3 (Analysis Depth)**: 1-2 weeks
- **v1.4 (Advanced Features)**: 2-4 weeks

**Total: 6-11 weeks (~2-3 months post-v1.0)**

---

## DECISION LOG

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-05-27 | Created FUTURE_VISION.md | Track "exceed The LOWDOWN" goals for v1.1+ |
| 2026-05-27 | Defer source expansion to v1.1 | v1.0 MVP ships with ISW alone, fix scrapers post-launch |
| 2026-05-27 | Defer PDF enhancement to v1.2 | ReportLab basic styling sufficient for v1.0 portfolio |
| 2026-05-27 | Defer advanced features to v1.4 | Focus on core briefing quality before adding bells/whistles |

---

## NOTES

- This roadmap is aspirational, not committed. v1.0 is the portfolio-ready milestone.
- Features beyond v1.0 depend on user feedback and personal bandwidth.
- Cost ceiling remains $20/month even with all enhancements.
- The LOWDOWN serves as a quality benchmark, not a direct competitor (we're mobile-first, they're email).
