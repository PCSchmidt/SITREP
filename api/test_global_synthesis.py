"""Test global synthesis end-to-end."""
import asyncio
import json
from pathlib import Path
from synthesis.bluf_synthesizer import BLUFSynthesizer


async def main():
    scraped_dir = Path("data/scraped")
    all_articles = []
    for f in scraped_dir.glob("*.json"):
        data = json.loads(f.read_text(encoding='utf-8'))
        if isinstance(data, list):
            all_articles.extend(data)
        elif isinstance(data, dict) and "articles" in data:
            all_articles.extend(data["articles"])

    print(f"Loaded {len(all_articles)} articles")

    synth = BLUFSynthesizer()
    briefing = await synth.synthesize_global(all_articles)

    print(f"\nRegion:  {briefing['region']}")
    print(f"BLUF:    {briefing['bluf'][:140]}...")
    print(f"Sections ({len(briefing['sections'])}):")
    for s in briefing["sections"]:
        print(f"  - {s['title']}")
    print(f"Key devs: {len(briefing['key_developments'])}")
    print(f"Articles: {briefing['article_count']}")
    print(f"Model:    {briefing['metadata']['model_used']}")

    # Save so /briefing/global can serve it
    Path("data/briefings").mkdir(parents=True, exist_ok=True)
    out = Path("data/briefings/global_20260529_000000.json")
    out.write_text(json.dumps(briefing, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"\nSaved to {out}")
    print("\n[PASS] Global synthesis working")


if __name__ == "__main__":
    asyncio.run(main())
