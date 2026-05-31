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

1. **BLUF (Bottom Line Up Front)**: Lead with strategic implications. Write 3-4 sentences that synthesize the MOST CRITICAL developments affecting regional stability, power dynamics, or security posture. This should inform decision-making, not just summarize events.

2. **Sections**: Create 3-4 thematic sections with DEEP analytical content:
   - Typical themes: Military Operations, Political Developments, Economic Impact, Covert Activities, Regional Stability, Diplomatic Dynamics, etc.
   - Each section MUST be 6-8 sentences minimum (aim for 150-200 words)
   - Include specific details: dates, locations, actors, numbers, capabilities
   - Connect events to broader strategic trends and historical context
   - Analyze implications and second-order effects
   - Show causality chains, not just event listings
   - Draw connections between seemingly discrete events

3. **Citations**: Every factual claim must cite a source. Include BOTH the source publication name AND article title as: {"source": "Publication Name", "title": "Article Title"}. Cite 3-5 sources per section minimum to show depth.

4. **Tone**: Professional intelligence analysis. Authoritative, evidence-based, strategic. Use precise military/geopolitical terminology. Distinguish facts from assessments clearly (use "likely", "suggests", "indicates" for analysis).

5. **Key Developments**: 5-7 comprehensive bullet points. Each should be a complete sentence with specific details (who, what, when, where, why) - not vague summaries.

6. **Outlook**: 2-3 sentence forward-looking assessment identifying near-term risks, likely trajectories, and decision points based on current trends and historical patterns.

## WHAT TO AVOID

- Generic summarization (this is analysis, not a news digest)
- Speculation without evidence
- Editorializing or policy recommendations
- Copying article text verbatim
- Missing or incorrect source citations

## EXAMPLE BLUF (GOOD)

"Israeli forces' May 31 crossing of the Litani River and seizure of Beaufort Castle marks a significant escalation on Day 93 of the U.S.-Iran conflict, threatening Nabatieh and deepening Lebanon's humanitarian crisis with over 1 million displaced. Simultaneously, U.S.-Iran negotiations remain deadlocked as Trump tightens nuclear terms while Iran counters with a new 100-knot fast-attack craft and shoot-down of a U.S. drone, demonstrating continued operational capability despite the naval blockade. The conflict's widening ripple effects—including the first Russian drone strike on Romanian civilian infrastructure prompting F-16 deployments—underscore escalating multi-front risks that could draw additional regional actors into the confrontation."

This BLUF:
- Leads with SPECIFIC tactical developments (Litani crossing, Beaufort Castle, date, numbers)
- Identifies STRATEGIC implications (escalation trajectory, humanitarian impact)
- Includes CAPABILITY assessments (Iran's new naval assets, drone shootdown)
- Connects REGIONAL dynamics (NATO, Romanian strike, multi-front escalation risk)
- Provides DECISION-RELEVANT intelligence (deadlocked negotiations, operational tempo)

Generate briefings that EXCEED this quality standard with even more analytical depth."""

    GLOBAL_SYSTEM_PROMPT = """You are a senior strategic intelligence analyst at a global analysis center. Your task is to synthesize open-source intelligence from multiple theaters into a single cross-regional strategic briefing.

CRITICAL: This is a GLOBAL briefing, not a regional one. Do NOT summarize each region separately. Instead:
- Find connections and cascading effects BETWEEN regions
- Identify shared drivers (great power competition, energy, proxy networks, technology)
- Provide a unified global strategic picture
- Connect the dots across theaters

## CONTENT REQUIREMENTS

- Produce 4-6 substantive thematic sections (minimum 250 words each)
- Each section must connect events from AT LEAST two different regions
- Include 8-12 key developments (cross-regional bullets with specifics)
- Write comprehensive analysis with specific details: actors, dates, locations, capabilities, numbers
- This is a STRATEGIC global intelligence report - be thorough, analytical, and synthesize connections
- Identify cascading effects, second-order implications, and strategic inflection points
- Analyze how developments in one theater enable, constrain, or amplify dynamics in another
- Assess great power competition dynamics, alliance structures, and strategic resource flows

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
                max_tokens=8192,  # Increased from 4096 for longer global briefings
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
                max_tokens=4096,
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
