# Open Router API client with multi-model waterfall
import os
import logging
from typing import Dict, List, Optional, Tuple
import httpx
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)


class OpenRouterClient:
    """
    Client for Open Router API with automatic model fallback.

    Waterfall order:
    1. DeepSeek V4 Flash ($0.10/$0.20 per 1M tokens) - ~$0.001/briefing
    2. DeepSeek V3.2 ($0.25/$0.38 per 1M tokens) - ~$0.003/briefing
    3. Kimi K2.5 ($0.40/$1.90 per 1M tokens) - ~$0.009/briefing

    Cost savings: 99.3% reduction vs GPT-4o Mini ($0.15 → $0.001 per briefing)
    """

    BASE_URL = "https://openrouter.ai/api/v1"

    # Model waterfall (in priority order)
    # All models validated 2026-05-23 with full BLUF synthesis tests
    MODELS = [
        {
            "id": "deepseek/deepseek-v4-flash",
            "name": "DeepSeek V4 Flash",
            "cost": "$0.001/briefing",  # $0.10/$0.20 per 1M tokens
            "max_tokens": 16384
        },
        {
            "id": "deepseek/deepseek-v3.2",
            "name": "DeepSeek V3.2",
            "cost": "$0.003/briefing",  # $0.25/$0.38 per 1M tokens
            "max_tokens": 16384
        },
        {
            "id": "moonshotai/kimi-k2.5",
            "name": "Kimi K2.5",
            "cost": "$0.009/briefing",  # $0.40/$1.90 per 1M tokens
            "max_tokens": 16384
        }
    ]

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OPENROUTER_API_KEY not found. "
                "Set it in .env or pass to constructor."
            )

        self.client = httpx.AsyncClient(timeout=120.0)
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://sitrep.app",  # Optional: your app URL
            "X-Title": "SITREP Intelligence Briefing"
        }

    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model_id: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 0.7
    ) -> Tuple[str, Dict]:
        """
        Send chat completion request to Open Router.

        Args:
            messages: List of message dicts with 'role' and 'content'
            model_id: Specific model to use (default: use waterfall)
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature (0-1)

        Returns:
            Tuple of (response_text, metadata)
        """
        if model_id:
            # Use specific model
            return await self._call_model(model_id, messages, max_tokens, temperature)
        else:
            # Try waterfall
            return await self._waterfall_completion(messages, max_tokens, temperature)

    async def _waterfall_completion(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int,
        temperature: float
    ) -> Tuple[str, Dict]:
        """Try models in waterfall order until one succeeds"""
        last_error = None

        for model in self.MODELS:
            try:
                logger.info(f"Trying {model['name']} ({model['cost']})...")
                response, metadata = await self._call_model(
                    model['id'], messages, max_tokens, temperature
                )
                logger.info(f"✓ Success with {model['name']}")
                metadata['model_used'] = model['name']
                metadata['cost_estimate'] = model['cost']
                return response, metadata

            except Exception as e:
                last_error = e
                logger.warning(f"✗ {model['name']} failed: {e}")
                continue

        # All models failed
        raise Exception(f"All models failed. Last error: {last_error}")

    async def _call_model(
        self,
        model_id: str,
        messages: List[Dict[str, str]],
        max_tokens: int,
        temperature: float
    ) -> Tuple[str, Dict]:
        """Make API call to specific model"""
        payload = {
            "model": model_id,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature
        }

        try:
            response = await self.client.post(
                f"{self.BASE_URL}/chat/completions",
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            data = response.json()

            # Extract response text
            content = data['choices'][0]['message']['content']

            # Some models intermittently return null content (e.g. content
            # filter, empty completion). Treat as a failure so the waterfall
            # falls through to the next model instead of propagating None.
            if not content:
                finish = data['choices'][0].get('finish_reason', 'unknown')
                raise Exception(f"{model_id} returned empty content (finish_reason={finish})")

            # Extract usage metadata
            usage = data.get('usage', {})
            metadata = {
                'model_id': model_id,
                'prompt_tokens': usage.get('prompt_tokens', 0),
                'completion_tokens': usage.get('completion_tokens', 0),
                'total_tokens': usage.get('total_tokens', 0),
                'finish_reason': data['choices'][0].get('finish_reason', 'unknown')
            }

            return content, metadata

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                raise Exception(f"Rate limit exceeded for {model_id}")
            elif e.response.status_code == 402:
                raise Exception(f"Insufficient credits for {model_id}")
            else:
                raise Exception(f"HTTP {e.response.status_code}: {e.response.text}")
        except Exception as e:
            raise Exception(f"API call failed: {str(e)}")

    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


# Example usage
async def test_client():
    """Test Open Router client"""
    async with OpenRouterClient() as client:
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say hello!"}
        ]

        response, metadata = await client.chat_completion(messages)
        print(f"Response: {response[:100]}...")  # Limit output to avoid encoding issues
        print(f"Model: {metadata.get('model_used', 'unknown')}")
        print(f"Tokens: {metadata['total_tokens']}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_client())
