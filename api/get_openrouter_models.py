# Get available models from OpenRouter API
import asyncio
import httpx
from dotenv import load_dotenv
import os
import json

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

async def get_models():
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(
                "https://openrouter.ai/api/v1/models",
                headers={"Authorization": f"Bearer {api_key}"}
            )
            if response.status_code == 200:
                models = response.json()
                # Filter for moonshot and deepseek
                print("DeepSeek Models:")
                print("-" * 80)
                for model in models.get("data", []):
                    if "deepseek" in model["id"].lower():
                        pricing = model.get("pricing", {})
                        print(f"ID: {model['id']}")
                        print(f"  Name: {model.get('name', 'N/A')}")
                        print(f"  Price: ${float(pricing.get('prompt', 0))*1000000:.2f}/${float(pricing.get('completion', 0))*1000000:.2f} per 1M tokens")
                        print(f"  Context: {model.get('context_length', 'N/A')} tokens")
                        print()
                
                print("\nMoonshot/Kimi Models:")
                print("-" * 80)
                found_moonshot = False
                for model in models.get("data", []):
                    if "moonshot" in model["id"].lower() or "kimi" in model["id"].lower():
                        found_moonshot = True
                        pricing = model.get("pricing", {})
                        print(f"ID: {model['id']}")
                        print(f"  Name: {model.get('name', 'N/A')}")
                        print(f"  Price: ${float(pricing.get('prompt', 0))*1000000:.2f}/${float(pricing.get('completion', 0))*1000000:.2f} per 1M tokens")
                        print(f"  Context: {model.get('context_length', 'N/A')} tokens")
                        print()
                
                if not found_moonshot:
                    print("No Moonshot/Kimi models found in API response")
                    
            else:
                print(f"Error: {response.status_code} - {response.text[:200]}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(get_models())
