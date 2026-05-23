# Open Router Setup Guide

## Quick Start (5 minutes)

### 1. Create Open Router Account
- Go to: https://openrouter.ai
- Sign up with Google/GitHub or email
- **No credit card required** for free tier models

### 2. Get API Key
- Navigate to: https://openrouter.ai/keys
- Click "Create Key"
- Copy your API key (starts with `sk-or-v1-...`)

### 3. Configure Environment
```bash
# In the api/ directory
cp .env.example .env

# Edit .env and add your key:
OPENROUTER_API_KEY=sk-or-v1-your-actual-key-here
```

### 4. Test the Integration
```bash
# From api/ directory
python synthesis/openrouter_client.py
```

Expected output:
```
Trying Gemini 2.0 Flash (free)...
✓ Success with Gemini 2.0 Flash
Response: Hello! How can I help you today?
Model: Gemini 2.0 Flash
Tokens: 28
```

---

## Model Waterfall

Your SITREP instance will try models in this order:

| Priority | Model | Cost | Use Case |
|----------|-------|------|----------|
| 1 | **Gemini 2.0 Flash** | FREE | Primary (1.5M requests/day) |
| 2 | **DeepSeek V3** | $0.014/briefing | Fallback if Gemini rate limit |
| 3 | **Kimi K2.5** | $0.30/briefing | Fallback if DeepSeek fails |
| 4 | **Claude Haiku 4.5** | $0.80/briefing | Emergency only |

**Expected cost**: $0/month (Gemini free tier handles everything)  
**Worst-case cost**: $1-2/month if you exceed Gemini limits

---

## Testing the Full Pipeline

Once Open Router is configured:

```bash
# Test BLUF synthesis with real ISW data
python synthesis/bluf_synthesizer.py
```

This will:
1. Load scraped ISW articles from `data/scraped/`
2. Send to Open Router (Gemini first)
3. Generate BLUF briefing for Europe/Africa region
4. Save to `data/briefings/europe_africa_2026-05-23.json`

---

## Troubleshooting

### Error: "OPENROUTER_API_KEY not found"
- Check that `.env` file exists in `api/` directory
- Verify the key is set: `OPENROUTER_API_KEY=sk-or-v1-...`
- Make sure there are no quotes around the key

### Error: "Rate limit exceeded"
- Gemini free tier: 1,500 requests/day
- Automatic fallback to DeepSeek V3 ($0.014/briefing)
- Check usage at: https://openrouter.ai/activity

### Error: "Insufficient credits"
- Gemini is free (no credits needed)
- DeepSeek/Kimi require credits (add $5 minimum)
- Add credits at: https://openrouter.ai/credits

---

## Next Steps

After Open Router is working:
1. ✅ Test synthesis with ISW data
2. Iterate on BLUF prompt quality (6-8h)
3. Expand to all 4 regions (Middle East, Indo-Pacific, Europe/Africa, Western Hemisphere)
4. Move to v0.3 (PDF generation)
