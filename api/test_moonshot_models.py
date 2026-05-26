# Test various Moonshot/Kimi model IDs
import asyncio
import httpx
from dotenv import load_dotenv
import os

load_dotenv()

# Common patterns for Moonshot models
models_to_test = [
    "moonshot/v1-8k",
    "moonshot/v1-32k", 
    "moonshot/v1-128k",
    "openai/moonshot-v1-8k",
    "kimi/v1-8k",
    "deepseek/deepseek-chat",
    "deepseek/deepseek-reasoner",
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
                    "messages": [{"role": "user", "content": "Hi"}],
                    "max_tokens": 5
                }
            )
            if response.status_code == 200:
                data = response.json()
                model_used = data.get("model", "unknown")
                print(f"[OK] {model_id} -> {model_used}")
                return True
            else:
                error_msg = response.text[:150]
                print(f"[FAIL] {model_id} - {response.status_code}: {error_msg}")
                return False
        except Exception as e:
            print(f"[ERROR] {model_id} - {str(e)[:100]}")
            return False

async def main():
    print("Testing Moonshot/Kimi and DeepSeek model IDs...\n")
    for model in models_to_test:
        await test_model(model)
        await asyncio.sleep(0.5)

if __name__ == "__main__":
    asyncio.run(main())
