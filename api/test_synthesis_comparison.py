# Compare GPT-4o Mini vs DeepSeek chat for BLUF synthesis
import asyncio
import json
from pathlib import Path
from synthesis.openrouter_client import OpenRouterClient

async def test_model(model_id: str, model_name: str):
    """Test a specific model with sample briefing synthesis"""
    print(f"\n{'='*60}")
    print(f"Testing: {model_name} ({model_id})")
    print(f"{'='*60}")
    
    # Load sample articles
    scraped_dir = Path("../data/scraped")
    all_articles = []
    for json_file in scraped_dir.glob("*.json"):
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, dict) and 'articles' in data:
                all_articles.extend(data['articles'][:3])  # Just first 3 for speed
    
    print(f"Loaded {len(all_articles)} articles for testing")
    
    # Create client
    client = OpenRouterClient()
    
    # Simple test prompt
    messages = [{
        "role": "user",
        "content": f"Summarize these articles in 50 words:\n\n{json.dumps(all_articles[:2], indent=2)[:500]}"
    }]
    
    try:
        response, metadata = await client.chat_completion(
            messages=messages,
            model_id=model_id  # Fixed parameter name
        )
        
        print(f"\n[SUCCESS] Response ({len(response)} chars):")
        print(f"{response[:200]}...")
        print(f"\nMetadata:")
        print(f"  Tokens: {metadata.get('prompt_tokens', 0)} prompt + {metadata.get('completion_tokens', 0)} completion")
        print(f"  Model: {metadata.get('model_used', 'unknown')}")
        print(f"  Cost estimate: ${metadata.get('cost_estimate', 0):.4f}")
        
        return True
    except Exception as e:
        print(f"\n[FAILED] Error: {str(e)}")
        return False

async def main():
    models = [
        ("openai/gpt-4o-mini", "GPT-4o Mini (current)"),
        ("deepseek/deepseek-chat", "DeepSeek Chat"),
    ]
    
    for model_id, model_name in models:
        await test_model(model_id, model_name)
        await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(main())
