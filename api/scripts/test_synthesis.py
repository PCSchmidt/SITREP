# Test BLUF synthesis with real ISW data
import asyncio
import json
import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.synthesis.openrouter_client import OpenRouterClient
from api.synthesis.bluf_synthesizer import BLUFSynthesizer


async def test_synthesis():
    """Test full synthesis pipeline"""
    print("=" * 60)
    print("SITREP BLUF Synthesis Test")
    print("=" * 60)

    # Load ISW data
    data_path = Path(__file__).parent.parent / "data" / "scraped" / "isw_2026-05-23.json"
    print(f"\n[1/4] Loading data from: {data_path}")

    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    articles = data['articles']
    print(f"  Loaded {len(articles)} articles from ISW")

    # Filter for Europe/Africa region (most articles are Ukraine/Russia)
    region = "Europe/Africa"
    region_articles = [a for a in articles if region in a.get('region_tags', [])]
    print(f"  Found {len(region_articles)} articles tagged with '{region}'")

    # Initialize synthesizer
    print(f"\n[2/4] Initializing BLUF synthesizer...")
    async with OpenRouterClient() as client:
        synthesizer = BLUFSynthesizer(openrouter_client=client)

        # Generate briefing
        print(f"\n[3/4] Generating briefing for {region}...")
        print(f"  Sending {len(region_articles[:10])} articles to LLM (limited to 10 for testing)")

        briefing = await synthesizer.synthesize_region(
            articles=articles,  # Pass all, let synthesizer filter
            region=region,
            max_articles=10
        )

    # Display results
    print(f"\n[4/4] Briefing generated successfully!")
    print("=" * 60)
    print(f"\nREGION: {briefing['region']}")
    print(f"\nBLUF:\n{briefing['bluf']}")
    print(f"\nSECTIONS ({len(briefing['sections'])}):")
    for i, section in enumerate(briefing['sections'], 1):
        print(f"\n  {i}. {section['title']}")
        print(f"     {section['content'][:150]}...")
        print(f"     Sources: {len(section.get('sources', []))} cited")

    if 'key_developments' in briefing:
        print(f"\nKEY DEVELOPMENTS:")
        for dev in briefing['key_developments']:
            print(f"  - {dev}")

    print(f"\nOUTLOOK:\n{briefing.get('outlook', 'N/A')}")

    # Metadata
    print("\n" + "=" * 60)
    print("METADATA:")
    meta = briefing.get('metadata', {})
    print(f"  Model: {meta.get('model_used', 'unknown')}")
    print(f"  Tokens: {meta.get('total_tokens', 0)}")
    print(f"  Cost estimate: {meta.get('cost_estimate', 'unknown')}")
    print(f"  Articles used: {briefing.get('article_count', 0)}")

    # Save briefing
    print(f"\n[SAVE] Saving briefing...")
    filepath = synthesizer.save_briefing(briefing)
    print(f"  Saved to: {filepath}")
    print("=" * 60)

    return briefing


if __name__ == "__main__":
    asyncio.run(test_synthesis())
