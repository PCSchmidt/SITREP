# SETUP_OPENROUTER

How to get an OpenRouter API key and point SITREP's synthesis client at it.

The production API **https://sitrep-production-6aac.up.railway.app** reads
`OPENROUTER_API_KEY` from its Railway variables and writes one briefing per desk through
`api/synthesis/openrouter_client.py`.

## Get a key

1. Sign in at https://openrouter.ai with Google, GitHub, or email.
2. Open https://openrouter.ai/keys and click Create Key.
3. Copy the value. It starts with `sk-or-v1-`.

## Configure the backend

```bash
cd api
cp .env.example .env
```

Then set the key in `.env`:

```
OPENROUTER_API_KEY=sk-or-v1-your-actual-key-here
```

No quotes, no trailing spaces. On Railway, set the same variable under Service, Variables.
See [DEPLOYMENT.md](../DEPLOYMENT.md) for the full variable list.

## Test the client

```bash
# from api/
python synthesis/openrouter_client.py
```

The module's `__main__` block sends one "Say hello!" message through the waterfall and
prints the answer, the model that produced it, and the token count. It needs a valid
`OPENROUTER_API_KEY` because it makes a real request.

## Model waterfall

`OpenRouterClient.MODELS` tries these models in order and stops at the first usable
response:

| Order | Model id | Stated cost per briefing | Notes |
| --- | --- | --- | --- |
| 1 | `deepseek/deepseek-v4-flash` | ~$0.001 | primary; wrote every regional briefing in the 2026-09-12 run |
| 2 | `deepseek/deepseek-v3.2` | ~$0.003 | first fallback |
| 3 | `moonshotai/kimi-k2.5` | ~$0.009 | last fallback |

All three are requested with `max_tokens: 16384`. An HTTP error, a rate limit, empty
content, or a filtered completion counts as a failure and falls through to the next model.
The model that actually answered is recorded in the briefing's `metadata.model_used`, so
the waterfall is visible in the stored output rather than assumed.

Observed cost for the 2026-09-12 run: roughly 10.6k to 16.7k tokens per regional briefing,
all on DeepSeek V4 Flash.

## Cost

| Item | Value |
| --- | --- |
| Typical run | 4 regional + 1 composite briefing, ~$0.001 each |
| Daily run cost | about $0.005 per day, ~$0.15/month |
| Ceiling | $20/month |
| Worst case | if the waterfall reaches Kimi, ~$0.009 per briefing |

## Troubleshooting

| Error | Cause | Fix |
| --- | --- | --- |
| `OPENROUTER_API_KEY not found` | No key in the environment or `.env` | Set the variable; run the script from `api/` so `.env` loads |
| `HTTP 401: Authentication failed` | Wrong or revoked key | Reissue at https://openrouter.ai/keys |
| `HTTP 429` or `rate limit exceeded` | Provider limit on the current model | The waterfall moves to the next model; check https://openrouter.ai/activity |
| `HTTP 402` or insufficient credits | Paid model with no balance | DeepSeek V4 Flash is cheap but not free; add credits at https://openrouter.ai/credits |
| Empty briefing body | Model returned no content | Counts as a failure and falls through; if all three fail, the pipeline reports the desk as an error |

The legacy scratch test `python synthesis/bluf_synthesizer.py` reads a scraped snapshot
from `../data/scraped/` that is not committed, so it only runs after a scrape. Use the
client test above, or trigger the pipeline to exercise synthesis end to end.

## See also

- [../README.md](../README.md) - what SITREP is and how to run it locally.
- [../DEPLOYMENT.md](../DEPLOYMENT.md) - Railway variables and the deploy runbook.
- [../DEPLOYMENT_CONFIG.md](../DEPLOYMENT_CONFIG.md) - configuration reference.
