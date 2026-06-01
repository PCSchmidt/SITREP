# Test synthesis standalone
import asyncio
import json
from pathlib import Path
from synthesis.bluf_synthesizer import BLUFSynthesizer

async def test():
    # Load scraped articles
    scraped_dir = Path("../data/scraped")
    all_articles = []
    for json_file in scraped_dir.glob("*.json"):
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                all_articles.extend(data)
            elif isinstance(data, dict) and 'articles' in data:
                all_articles.extend(data['articles'])
            else:
                raise ValueError(f"Unexpected JSON format in {json_file.name}")

    print(f"Loaded {len(all_articles)} articles")

    # Synthesize
    synthesizer = BLUFSynthesizer()
    briefing = await synthesizer.synthesize_region(all_articles, "Europe/Africa")

    print(f"Briefing generated: {briefing['region']}")
    print(f"BLUF: {briefing['bluf'][:100]}...")
    return briefing

if __name__ == "__main__":
    result = asyncio.run(test())
    print("SUCCESS")
