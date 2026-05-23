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
  "region": "Middle East",
  "bluf": "2-3 sentence executive summary highlighting the most critical developments and their strategic implications.",
  "sections": [
    {
      "title": "Covert Operations",
      "content": "Detailed analysis paragraph covering this topic. Include specific facts, dates, and actors. Connect events to strategic trends.",
      "sources": ["Article title 1", "Article title 2"]
    },
    {
      "title": "Military Operations",
      "content": "...",
      "sources": ["..."]
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

1. **BLUF (Bottom Line Up Front)**: Start with the most important takeaway. What does leadership need to know RIGHT NOW?

2. **Sections**: Create 2-4 thematic sections based on the content:
   - Typical themes: Military Operations, Political Developments, Economic Impact, Covert Activities, Regional Stability, etc.
   - Each section should be 3-5 sentences of substantive analysis
   - Connect dots between articles - show trends, not just events

3. **Citations**: Every claim must trace back to a source article. Use article titles in the "sources" array.

4. **Tone**: Professional, analytical, factual. Avoid speculation unless clearly labeled as assessment.

5. **Key Developments**: 3-5 bullet points capturing the most significant events from the articles.

6. **Outlook**: Brief forward-looking statement based on current trends.

## WHAT TO AVOID

- Generic summarization (this is analysis, not a news digest)
- Speculation without evidence
- Editorializing or policy recommendations
- Copying article text verbatim
- Missing or incorrect source citations

## EXAMPLE BLUF

"U.S.-Israel military coordination intensifies as Iran's proxy operations expand across the Red Sea corridor. Economic blockades are constraining Tehran's ability to sustain multi-theater operations, but decentralized command structures among Houthi forces suggest near-term escalation risk remains elevated despite strategic pressure."

This BLUF:
- Leads with the strategic picture (U.S.-Israel coordination + Iran proxy expansion)
- Identifies the constraint (economic pressure)
- Assesses near-term risk (escalation despite pressure)
- Is specific enough to inform decision-making

Generate briefings that match this quality standard."""

    def __init__(self, openrouter_client: Optional[OpenRouterClient] = None):
        self.client = openrouter_client

    async def synthesize_region(
        self,
        articles: List[Dict],
        region: str = "Middle East",
        max_articles: int = 15
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
        # Filter and limit articles
        region_articles = [
            a for a in articles
            if region in a.get('region_tags', [])
        ][:max_articles]

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
