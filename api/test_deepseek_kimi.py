# Test DeepSeek and Kimi model availability on OpenRouter
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

# Potential model IDs to test
models_to_test = [
    # DeepSeek variants
    "deepseek/deepseek-chat",
    "deepseek/deepseek-v3",
    "deepseek/deepseek-coder",
    # Kimi variants  
    "moonshot/moonshot-v1-8k",
    "moonshot/moonshot-v1-32k",
    "moonshot/moonshot-v1-128k",
    "kimi/moonshot-v1-8k",
]

api_key = os.getenv("OPENROUTER_API_KEY")

async def test_model(model_id: str):
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model_id,
                    "messages": [{"role": "user", "content": "Test"}],
                    "max_tokens": 10
                }
            )
            if response.status_code == 200:
                print(f"[OK] {model_id} - WORKS")
                return True
            else:
                print(f"[FAIL] {model_id} - {response.status_code}: {response.text[:100]}")
                return False
        except Exception as e:
            print(f"[ERROR] {model_id} - {str(e)[:100]}")
            return False

async def main():
    import asyncio
    print("Testing DeepSeek and Kimi models on OpenRouter...\n")
    for model in models_to_test:
        await test_model(model)
        await asyncio.sleep(1)  # Rate limiting

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
