# BLUF (Bottom Line Up Front) briefing synthesizer
import json
import logging
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path

from .openrouter_client import OpenRouterClient

logger = logging.getLogger(__name__)


class BLUFSynthesizer:
    """
    Synthesizes intelligence briefings in BLUF format from scraped articles.

    Output format matches military intelligence products:
    - Executive summary (BLUF)
    - Regional analysis sections
    - Numbered sub-sections with detailed analysis
    - Source citations
    """

    # System prompt defining BLUF format and tone
    SYSTEM_PROMPT = """You are an intelligence analyst for SITREP, a military-grade geopolitical intelligence platform.

Your task is to synthesize open-source news articles into professional intelligence briefings using the BLUF (Bottom Line Up Front) format.

## OUTPUT FORMAT

Generate a JSON object with this exact structure:

```json
{
  "region": "<REGION_NAME>",
  "bluf": "2-3 sentence executive summary highlighting the most critical developments and their strategic implications.",
  "sections": [
    {
      "title": "Covert Operations",
      "content": "Detailed analysis paragraph covering this topic. Include specific facts, dates, and actors. Connect events to strategic trends.",
      "sources": [
        {"source": "Foreign Policy", "title": "Article title 1"},
        {"source": "The War Zone", "title": "Article title 2"}
      ]
    },
    {
      "title": "Military Operations",
      "content": "...",
      "sources": [
        {"source": "ISW", "title": "..."}
      ]
    }
  ],
  "key_developments": [
    "Bullet point summary 1",
    "Bullet point summary 2",
    "Bullet point summary 3"
  ],
  "outlook": "1-2 sentence forward-looking assessment of likely near-term developments.",
  "generated_at": "2026-05-23T12:00:00Z"
}
```

## ANALYSIS GUIDELINES

0. **Region Field**: CRITICAL - Set the "region" field to EXACTLY match the region name specified in the user prompt. Do NOT shorten or modify it (e.g., if user says "Europe/Africa", use "Europe/Africa" not "Europe").

1. **BLUF (Bottom Line Up Front)**: Lead with comprehensive strategic assessment. Write 5-7 sentences that synthesize:
   - The MOST CRITICAL military/security developments
   - Political and economic factors driving or constraining those developments
   - Second-order effects and cascade risks
   - Strategic implications for regional stability and great power competition
   This should be decision-quality intelligence, not event summary.

2. **Sections**: Create 4-6 thematic sections with COMPREHENSIVE analytical depth:
   - REQUIRED: At least ONE section must focus on "Economic & Resource Competition" or "Socio-Economic Factors" analyzing trade, sanctions, energy, resources, debt, inflation, demographics, migration, or economic warfare
   - Other themes to consider: Military Operations, Political/Diplomatic Dynamics, Covert/Intelligence Activities, Regional Stability, Humanitarian/Social Crises
   - Each section MUST be 10-20 sentences (aim for 300-500 words)
   - Include granular specifics: exact dates, precise locations, named actors, quantified capabilities, dollar amounts
   - Integrate socio-economic analysis: How do economic conditions, resource scarcity, demographic pressures, or social movements enable, constrain, or amplify military/political developments?
   - Connect events to broader strategic trends and historical precedents
   - Analyze multi-order effects: immediate impact → second-order consequences → strategic trajectory shifts
   - Show causality chains with evidence, not just chronology
   - Synthesize connections across military, political, economic, and social domains

3. **Citations**: Every factual claim needs attribution. Include source name, article title, AND URL when available: {"source": "Publication", "title": "Article Title", "url": "https://..."}. Cite 5-8 sources per section to demonstrate thorough research.

4. **Tone**: Professional intelligence analysis at strategic level. Authoritative, evidence-based, multi-domain. Use precise terminology (military, economic, political). Clearly distinguish verified facts from analytical assessments (use "likely", "suggests", "indicates", "assess that" for analysis).

5. **Key Developments**: 7-10 comprehensive bullet points. Each must be a complete, detailed sentence with:
   - Specific actors and their roles
   - Precise timing and location
   - Quantified impact where applicable
   - Why it matters strategically
   Not vague event listings—each should read like a mini-analysis.

6. **Outlook**: 3-5 sentence forward-looking strategic assessment:
   - Near-term risks and inflection points (next 30-90 days)
   - Likely trajectories based on current trends and constraints
   - Key decision points or trigger events to monitor
   - Potential black swans or low-probability high-impact scenarios
   Ground assessments in historical patterns and current evidence.

## WHAT TO AVOID

- Generic summarization (this is analysis, not a news digest)
- Speculation without evidence
- Editorializing or policy recommendations
- Copying article text verbatim
- Missing or incorrect source citations

## EXAMPLE BLUF (EXCELLENT - WITH ECONOMIC INTEGRATION)

"Israeli forces' May 31 crossing of the Litani River marks a significant escalation on Day 93 of the U.S.-Iran conflict, threatening Nabatieh and deepening Lebanon's humanitarian crisis with over 1 million displaced. The mutual blockade—U.S. naval cordon on Iranian ports and Iran's Strait of Hormuz closure—has driven oil prices to $147/barrel and triggered UN warnings of a looming global food crisis as 40% of seaborne grain shipments remain stuck. U.S.-Iran negotiations are deadlocked over conflicting demands: Washington seeks a 20-year uranium enrichment freeze while Tehran demands $250 billion in war reparations and full sanctions relief, with both sides constrained by domestic political pressures ahead of U.S. midterms and Iran's Assembly of Experts succession crisis. Iran's unveiling of a 100-knot fast-attack craft and successful drone shootdown demonstrates retained operational capability despite three months of sustained bombardment, while the conflict's economic ripple effects—Romanian inflation hitting 34% after Russian drone strikes disrupted Black Sea shipping—illustrate how localized military actions cascade into region-wide socio-economic instability. The strategic calculus now centers on whether economic pain (Iranian GDP contracted 18% in Q2) forces compromise before Winter 2026-27 energy shortages trigger European political fractures."

This BLUF:
- Leads with SPECIFIC tactical developments (Litani crossing, date, displacement numbers)
- Integrates ECONOMIC drivers (oil at $147/bbl, grain shipments, GDP contraction 18%)
- Connects MILITARY capabilities to ECONOMIC constraints (operational capability despite bombardment vs. economic pain forcing compromise)
- Analyzes POLITICAL pressures from ECONOMIC conditions (midterms, succession crisis, European energy shortages)
- Shows CASCADING economic effects across regions (Romanian inflation from Black Sea disruption)
- Provides DECISION-RELEVANT intelligence grounded in multi-domain reality (strategic calculus balancing military capability vs. economic pressure)

Generate briefings that EXCEED this quality standard with even more analytical depth."""

    GLOBAL_SYSTEM_PROMPT = """You are a senior strategic intelligence analyst at a global analysis center. Your task is to synthesize open-source intelligence from multiple theaters into a single cross-regional strategic briefing.

CRITICAL: This is a GLOBAL briefing, not a regional one. Do NOT summarize each region separately. Instead:
- Find connections and cascading effects BETWEEN regions
- Identify shared drivers (great power competition, energy, proxy networks, technology)
- Provide a unified global strategic picture
- Connect the dots across theaters

## CONTENT REQUIREMENTS

- Produce 5-7 substantive thematic sections (minimum 400-600 words each)
- Each section must connect events from AT LEAST two different regions, showing causal links
- Include 10-15 key developments (cross-regional bullets with specific actors, dates, impacts)
- Write comprehensive multi-domain analysis: military, political, economic, social factors
- Integrate socio-economic drivers: How do economic conditions, resource competition, trade flows, demographic pressures, or social movements shape or constrain strategic behavior across regions?
- This is a STRATEGIC global intelligence report for senior decision-makers - maximize analytical depth
- Identify cascading effects, second-order implications, and strategic inflection points
- Analyze how developments in one theater enable, constrain, or amplify dynamics in another
- Assess great power competition dynamics, alliance structures, strategic resource flows, and economic warfare
- Connect military operations to their economic drivers and political constraints

## OUTPUT FORMAT

Generate a JSON object with this exact structure:

```json
{
  "region": "Global",
  "bluf": "3-4 sentence executive summary of the most significant cross-regional strategic developments and their global implications.",
  "sections": [
    {
      "title": "Thematic Cross-Regional Title",
      "content": "Comprehensive analysis connecting events across multiple regions (300+ words). Identify how actions in one theater affect others. Include specific actors, timelines, and strategic implications.",
      "sources": ["Article title 1", "Article title 2", "Article title 3"]
    }
  ],
  "key_developments": [
    "Cross-regional bullet 1 with specific details",
    "Cross-regional bullet 2 with specific details",
    "... (8-12 total bullets)"
  ],
  "outlook": "Global strategic forecast (200+ words): what the combined picture means for the next 30-90 days. Be specific about escalation risks, alliance dynamics, and probable courses of action.",
  "generated_at": "2026-01-01T00:00:00Z"
}
```

## SECTION THEMES (use the most relevant 3-4)

Good global section themes:
- **Great Power Competition** — US-China-Russia strategic maneuvering across theaters
- **Proxy Warfare Networks** — Iran, Russia, and non-state actors operating across regions
- **Energy and Economic Warfare** — sanctions, pipelines, chokepoints, supply chain as weapons
- **Technology and Emerging Domains** — drones, cyber, space, AI across multiple theaters
- **Alliance Dynamics** — NATO, Indo-Pacific partnerships, normalization deals
- **Nuclear and Escalation Risk** — posturing, doctrine shifts, red lines across regions

## ANALYSIS GUIDELINES

0. **Region Field**: ALWAYS set "region" to exactly "Global".
1. **Connect the dots**: A drone attack in the Strait of Hormuz affects energy prices in Europe. Russia's nuclear posturing enables Iran's boldness. Cite these linkages explicitly.
2. **Thematic, not regional**: Do NOT have sections titled "Europe/Africa" or "Middle East". Use strategic themes.
3. **3-4 sections max**: Focus on the highest-impact cross-regional dynamics.
4. **5 key developments max**: These should be the single most important facts a senior decision-maker needs.
5. **Source every claim**: Cite article titles in the sources array.

## WHAT TO AVOID

- Listing each region's news separately (that's a regional briefing, not a global one)
- Generic observations without cross-regional connections
- More than 4 sections (keep it tight and high-impact)"""

    def __init__(self, openrouter_client: Optional[OpenRouterClient] = None):
        self.client = openrouter_client

    async def synthesize_global(
        self,
        articles: List[Dict],
        articles_per_region: int = 12
    ) -> Dict:
        """
        Generate a cross-regional global BLUF briefing from all scraped articles.

        Takes the top N articles per region to ensure balanced coverage, then
        synthesizes a thematic cross-regional analysis.

        Args:
            articles: All scraped articles (all regions combined)
            articles_per_region: Max articles to include per region (default 12)

        Returns:
            Global briefing dict with cross-regional thematic sections
        """
        REGIONS = ["Middle East", "Indo-Pacific", "Europe/Africa", "Western Hemisphere"]

        # Take top N articles per region for balanced coverage
        selected: List[Dict] = []
        for region in REGIONS:
            region_articles = [
                a for a in articles
                if region in a.get('region_tags', [])
            ][:articles_per_region]
            selected.extend(region_articles)

        # Also include any "Global" tagged articles
        global_articles = [
            a for a in articles
            if a.get('region_tags') == ['Global'] or 'Global' in a.get('region_tags', [])
        ][:8]
        selected.extend(global_articles)

        if not selected:
            logger.warning("No articles available for global synthesis")
            return self._empty_briefing("Global")

        logger.info(f"Global synthesis: {len(selected)} articles across {len(REGIONS)} regions")

        user_prompt = self._build_global_prompt(selected)
        messages = [
            {"role": "system", "content": self.GLOBAL_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]

        async with self.client or OpenRouterClient() as client:
            response_text, metadata = await client.chat_completion(
                messages=messages,
                max_tokens=16000,  # cross-regional global briefing is the largest; was truncating at 8192
                temperature=0.7
            )

        try:
            cleaned = response_text.strip()
            if cleaned.startswith('```json'):
                cleaned = cleaned[7:]
            if cleaned.startswith('```'):
                cleaned = cleaned[3:]
            if cleaned.endswith('```'):
                cleaned = cleaned[:-3]
            cleaned = cleaned.strip()

            briefing = json.loads(cleaned)
            briefing['region'] = 'Global'  # Always force correct region name
            briefing['metadata'] = metadata
            briefing['article_count'] = len(selected)
            return briefing
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse global synthesis response: {e}")
            raise

    def _build_global_prompt(self, articles: List[Dict]) -> str:
        """Build the user prompt for global synthesis, grouped by region."""
        REGIONS = ["Middle East", "Indo-Pacific", "Europe/Africa", "Western Hemisphere", "Global"]

        prompt_parts = [
            "Synthesize the following open-source intelligence articles into a cross-regional GLOBAL strategic briefing. "
            "Identify connections BETWEEN regions, not just within them.\n"
        ]

        for region in REGIONS:
            region_articles = [a for a in articles if region in a.get('region_tags', [])]
            if not region_articles:
                continue
            prompt_parts.append(f"\n## {region} Articles\n")
            for i, article in enumerate(region_articles, 1):
                content = article['content'][:2500]  # Increased from 1500 to 2500
                prompt_parts.append(
                    f"### {region} Article {i}: {article['title']}\n"
                    f"Source: {article['source']}\n"
                    f"Content:\n{content}\n"
                )

        prompt_parts.append(
            "\n---\n\n"
            "Now synthesize these articles into a cross-regional GLOBAL intelligence briefing. "
            "Focus on connections BETWEEN regions. Return ONLY the JSON object."
        )

        return "\n".join(prompt_parts)

    async def synthesize_region(
        self,
        articles: List[Dict],
        region: str = "Middle East",
        max_articles: int = 30
    ) -> Dict:
        """
        Generate BLUF briefing for a specific region.

        Args:
            articles: List of article dicts (from scraper JSON)
            region: Geographic region to focus on
            max_articles: Limit number of articles to prevent token overflow

        Returns:
            Briefing dict with BLUF, sections, sources
        """
        # Filter articles for this region
        region_articles = [
            a for a in articles
            if region in a.get('region_tags', [])
        ]

        # Prioritize source diversity: take max N per source to avoid ISW dominance
        from collections import defaultdict
        by_source = defaultdict(list)
        for article in region_articles:
            by_source[article.get('source', 'Unknown')].append(article)

        # Take up to 5 articles per source, interleaved
        balanced_articles = []
        max_per_source = 5
        for source in sorted(by_source.keys()):  # Sort for consistency
            balanced_articles.extend(by_source[source][:max_per_source])

        # Limit total
        region_articles = balanced_articles[:max_articles]

        if not region_articles:
            logger.warning(f"No articles found for region: {region}")
            return self._empty_briefing(region)

        logger.info(f"Synthesizing {len(region_articles)} articles for {region}")

        # Build user prompt with article content
        user_prompt = self._build_article_prompt(region_articles, region)

        # Call LLM
        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]

        async with self.client or OpenRouterClient() as client:
            response_text, metadata = await client.chat_completion(
                messages=messages,
                max_tokens=12000,  # deep sections (5+ x 300-500 words) overflow 4096 -> truncated JSON
                temperature=0.7
            )

        # Parse JSON response (strip markdown code fences if present)
        try:
            # Remove markdown code fences if present
            cleaned_response = response_text.strip()
            if cleaned_response.startswith('```json'):
                cleaned_response = cleaned_response[7:]  # Remove ```json
            if cleaned_response.startswith('```'):
                cleaned_response = cleaned_response[3:]  # Remove ```
            if cleaned_response.endswith('```'):
                cleaned_response = cleaned_response[:-3]  # Remove trailing ```
            cleaned_response = cleaned_response.strip()

            briefing = json.loads(cleaned_response)
            # Force correct region name (LLMs sometimes shorten "Europe/Africa" to "Europe")
            briefing['region'] = region
            briefing['metadata'] = metadata
            briefing['article_count'] = len(region_articles)
            return briefing
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {e}")
            logger.error(f"Response text: {response_text[:500]}...")
            raise

    def _build_article_prompt(self, articles: List[Dict], region: str) -> str:
        """Construct user prompt with article summaries"""
        prompt_parts = [
            f"Generate a BLUF intelligence briefing for the **{region}** region based on these articles:\n"
        ]

        for i, article in enumerate(articles, 1):
            # Truncate very long articles to fit in context
            content = article['content'][:2000]
            prompt_parts.append(
                f"## Article {i}: {article['title']}\n"
                f"Source: {article['source']}\n"
                f"Date: {article['published_date']}\n"
                f"Content:\n{content}\n"
            )

        prompt_parts.append(
            "\n---\n\n"
            "Now synthesize these articles into a professional BLUF briefing. "
            "Return ONLY the JSON object, no additional text."
        )

        return "\n".join(prompt_parts)

    def _empty_briefing(self, region: str) -> Dict:
        """Return empty briefing when no articles available"""
        return {
            "region": region,
            "bluf": f"No recent intelligence available for {region}.",
            "sections": [],
            "key_developments": [],
            "outlook": "Insufficient data for forward assessment.",
            "generated_at": datetime.utcnow().isoformat(),
            "article_count": 0
        }

    def save_briefing(self, briefing: Dict, output_dir: str = "data/briefings"):
        """Save briefing to JSON file"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.utcnow().strftime("%Y-%m-%d")
        region_slug = briefing['region'].lower().replace(' ', '_').replace('/', '_')
        filename = f"{region_slug}_{timestamp}.json"
        filepath = output_path / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(briefing, f, indent=2, ensure_ascii=False)

        logger.info(f"Saved briefing to {filepath}")
        return str(filepath)


# Example usage
async def test_synthesizer():
    """Test BLUF synthesizer with sample data"""
    # Load scraped ISW data
    import json
    with open("../data/scraped/isw_2026-05-23.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    articles = data['articles']

    # Synthesize briefing
    synthesizer = BLUFSynthesizer()
    briefing = await synthesizer.synthesize_region(articles, region="Europe/Africa")

    # Print results
    print("\n=== GENERATED BRIEFING ===")
    print(f"Region: {briefing['region']}")
    print(f"\nBLUF: {briefing['bluf']}")
    print(f"\nSections: {len(briefing['sections'])}")
    for section in briefing['sections']:
        print(f"  - {section['title']}")
    print(f"\nModel: {briefing['metadata'].get('model_used', 'unknown')}")
    print(f"Tokens: {briefing['metadata']['total_tokens']}")

    # Save
    synthesizer.save_briefing(briefing)


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_synthesizer())
