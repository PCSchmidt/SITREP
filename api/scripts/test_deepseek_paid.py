# Test paid DeepSeek models
import asyncio
import json
from pathlib import Path
from synthesis.bluf_synthesizer import BLUFSynthesizer
from synthesis.openrouter_client import OpenRouterClient

async def quick_test(model_id: str, model_name: str):
    """Quick synthesis test"""
    print(f"\nTesting: {model_name} ({model_id})")
    
    scraped_dir = Path("../data/scraped")
    all_articles = []
    for json_file in scraped_dir.glob("*.json"):
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, dict) and 'articles' in data:
                all_articles.extend(data['articles'])
    
    original_models = OpenRouterClient.MODELS
    OpenRouterClient.MODELS = [{"id": model_id, "name": model_name, "cost": "test", "max_tokens": 16384}]
    
    try:
        synthesizer = BLUFSynthesizer()
        briefing = await synthesizer.synthesize_region(all_articles, "Europe/Africa")
        
        meta = briefing.get('metadata', {})
        print(f"  [OK] Sections: {len(briefing['sections'])}, Tokens: {meta.get('total_tokens', 0):,}")
        return True
    except Exception as e:
        print(f"  [FAIL] {str(e)[:100]}")
        return False
    finally:
        OpenRouterClient.MODELS = original_models

async def main():
    models = [
        ("deepseek/deepseek-v4-flash", "DeepSeek V4 Flash"),
        ("deepseek/deepseek-chat", "DeepSeek Chat (V3)"),
        ("deepseek/deepseek-v3.2", "DeepSeek V3.2"),
    ]
    
    for model_id, model_name in models:
        await quick_test(model_id, model_name)
        await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(main())
