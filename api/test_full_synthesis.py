# Full BLUF synthesis comparison
import asyncio
import json
from pathlib import Path
from synthesis.bluf_synthesizer import BLUFSynthesizer
from synthesis.openrouter_client import OpenRouterClient

async def test_full_synthesis(model_id: str, model_name: str):
    """Test full BLUF synthesis with specific model"""
    print(f"\n{'='*70}")
    print(f"Testing Full Synthesis: {model_name}")
    print(f"{'='*70}\n")
    
    # Load articles
    scraped_dir = Path("../data/scraped")
    all_articles = []
    for json_file in scraped_dir.glob("*.json"):
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, dict) and 'articles' in data:
                all_articles.extend(data['articles'])
    
    print(f"Loaded {len(all_articles)} articles")
    
    # Override the model list temporarily
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
        
        print(f"[SUCCESS] Generated briefing:")
        print(f"  BLUF: {briefing['bluf'][:150]}...")
        print(f"  Sections: {len(briefing['sections'])}")
        print(f"  Key developments: {len(briefing['key_developments'])}")
        print(f"\n  Metadata:")
        if 'metadata' in briefing:
            meta = briefing['metadata']
            print(f"    Model: {meta.get('model_used', 'unknown')}")
            print(f"    Tokens: {meta.get('prompt_tokens', 0)} + {meta.get('completion_tokens', 0)} = {meta.get('total_tokens', 0)}")
            print(f"    Cost: ${meta.get('cost_estimate', 0):.4f}")
        
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
        ("deepseek/deepseek-chat", "DeepSeek Chat"),
        ("openai/gpt-4o-mini", "GPT-4o Mini"),
    ]
    
    results = {}
    for model_id, model_name in models:
        result = await test_full_synthesis(model_id, model_name)
        results[model_name] = result
        await asyncio.sleep(3)
    
    print(f"\n{'='*70}")
    print("COMPARISON SUMMARY")
    print(f"{'='*70}")
    for name, result in results.items():
        if result:
            print(f"\n{name}:")
            print(f"  BLUF length: {len(result.get('bluf', ''))} chars")
            print(f"  Sections: {len(result.get('sections', []))}")
            if 'metadata' in result:
                print(f"  Cost: ${result['metadata'].get('cost_estimate', 0):.4f}")

if __name__ == "__main__":
    asyncio.run(main())
