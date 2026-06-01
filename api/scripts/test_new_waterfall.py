# Test new waterfall: DeepSeek V4 Flash Free + Kimi K2.5
import asyncio
import json
from pathlib import Path
from synthesis.bluf_synthesizer import BLUFSynthesizer
from synthesis.openrouter_client import OpenRouterClient

async def test_model(model_id: str, model_name: str):
    """Test full BLUF synthesis with specific model"""
    print(f"\n{'='*70}")
    print(f"Testing: {model_name}")
    print(f"Model ID: {model_id}")
    print(f"{'='*70}\n")
    
    # Load articles
    scraped_dir = Path("../data/scraped")
    all_articles = []
    for json_file in scraped_dir.glob("*.json"):
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, dict) and 'articles' in data:
                all_articles.extend(data['articles'])
    
    print(f"Loaded {len(all_articles)} articles\n")
    
    # Override model list
    original_models = OpenRouterClient.MODELS
    OpenRouterClient.MODELS = [{
        "id": model_id,
        "name": model_name,
        "cost": "testing",
        "max_tokens": 16384
    }]
    
    try:
        synthesizer = BLUFSynthesizer()
        briefing = await synthesizer.synthesize_region(all_articles, "Europe/Africa")
        
        print(f"[SUCCESS]\n")
        print(f"BLUF ({len(briefing['bluf'])} chars):")
        print(f"{briefing['bluf'][:200]}...\n")
        print(f"Sections: {len(briefing['sections'])}")
        for i, section in enumerate(briefing['sections'], 1):
            print(f"  {i}. {section['title']} ({len(section['content'])} chars)")
        print(f"\nKey Developments: {len(briefing['key_developments'])}")
        
        if 'metadata' in briefing:
            meta = briefing['metadata']
            print(f"\nMetadata:")
            print(f"  Model: {meta.get('model_used', 'unknown')}")
            print(f"  Tokens: {meta.get('total_tokens', 0):,}")
            print(f"  Prompt: {meta.get('prompt_tokens', 0):,}")
            print(f"  Completion: {meta.get('completion_tokens', 0):,}")
        
        return briefing
    except Exception as e:
        print(f"[FAILED] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return None
    finally:
        OpenRouterClient.MODELS = original_models

async def main():
    models = [
        ("deepseek/deepseek-v4-flash:free", "DeepSeek V4 Flash (FREE)"),
        ("moonshotai/kimi-k2.5", "Kimi K2.5"),
    ]
    
    results = {}
    for model_id, model_name in models:
        result = await test_model(model_id, model_name)
        results[model_name] = result
        await asyncio.sleep(3)
    
    print(f"\n{'='*70}")
    print("QUALITY COMPARISON")
    print(f"{'='*70}")
    for name, result in results.items():
        if result:
            print(f"\n{name}:")
            print(f"  BLUF: {len(result.get('bluf', ''))} chars")
            print(f"  Sections: {len(result.get('sections', []))}")
            print(f"  Key Developments: {len(result.get('key_developments', []))}")
            if 'metadata' in result:
                print(f"  Tokens: {result['metadata'].get('total_tokens', 0):,}")

if __name__ == "__main__":
    asyncio.run(main())
