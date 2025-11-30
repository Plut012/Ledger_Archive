# API Key Setup Guide

## Quick Setup

### 1. Choose Your Provider

**Anthropic Claude (Recommended)**
- Fast, efficient, great for character dialogue
- Haiku model available on all API tiers (including free)
- Get API key: https://console.anthropic.com/

**OpenAI**
- GPT-4 or GPT-3.5-turbo
- Get API key: https://platform.openai.com/api-keys

**Local (Ollama)**
- Free, runs on your machine
- Install: https://ollama.ai

### 2. Create .env File

**IMPORTANT:** Place `.env` in the **project root** (where README.md is), NOT in backend/.

```bash
cd /path/to/chain  # Project root
cp backend/.env.example .env
```

### 3. Add Your API Key

Edit `.env` with your chosen provider:

#### Anthropic Claude
```bash
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
LLM_PROVIDER=anthropic
```

#### OpenAI
```bash
OPENAI_API_KEY=sk-your-actual-key-here
LLM_PROVIDER=openai
```

#### Local (Ollama)
```bash
# First: ollama pull llama2
OPENAI_API_KEY=dummy
OPENAI_BASE_URL=http://localhost:11434/v1
OPENAI_MODEL=llama2
LLM_PROVIDER=openai-compatible
```

### 4. Verify Setup

Test your configuration:

```bash
cd backend
uv run python test_llm_connection.py
```

You should see:
```
✓ LLM client initialized
✓ Response: Hello from Claude!
✓ Streaming complete
✓ All LLM tests passed!
```

## Security

### Git Ignore
✅ `.env` is already in `.gitignore`
✅ Your API key will NOT be committed to git
✅ Safe to add real credentials

Verify:
```bash
git check-ignore -v .env
# Should output: .gitignore:26:.env	.env
```

### Best Practices
- Never commit `.env` files
- Never share your API keys
- Rotate keys if accidentally exposed
- Use environment variables in production

## Model Selection

### Anthropic Claude Models

**Haiku** (Default - Available on ALL tiers)
```bash
ANTHROPIC_MODEL=claude-3-haiku-20240307
```
- Fast responses (best for real-time chat)
- Cost-effective
- Excellent for character dialogue

**Sonnet** (Tier 2+ required)
```bash
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
```
- Better reasoning
- More nuanced responses
- Higher cost

**Opus** (Tier 2+ required)
```bash
ANTHROPIC_MODEL=claude-3-opus-20240229
```
- Most capable
- Slowest responses
- Highest cost

### Model Not Found Error?

If you get a 404 error with a specific model:
1. Check your API tier at https://console.anthropic.com/
2. Free tier only has access to Haiku
3. Use default (Haiku) or upgrade tier

## Testing Different Providers

Test which models work with your API key:

```bash
uv run python backend/test_model_discovery.py
```

## Troubleshooting

### Error: "Could not resolve authentication method"
- Check `.env` is in project root (not backend/)
- Verify API key is set correctly
- No spaces around `=` in `.env`

### Error: "model: claude-3-... not found"
- Your API tier doesn't have access to that model
- Use `claude-3-haiku-20240307` (works on all tiers)
- Or upgrade your API tier

### Error: "No module named 'anthropic'"
```bash
uv pip install -r backend/requirements.txt
```

### .env not being loaded
- Must be in project root: `/path/to/chain/.env`
- Check file exists: `ls -la .env`
- Check it's not in backend: `ls backend/.env` should fail

## Provider Comparison

| Provider | Cost | Speed | Quality | Setup |
|----------|------|-------|---------|-------|
| Claude Haiku | $ | Fast | Good | Easy |
| Claude Sonnet | $$ | Medium | Great | Tier 2+ |
| GPT-4 | $$$ | Slow | Great | Easy |
| GPT-3.5-turbo | $ | Fast | Good | Easy |
| Ollama (local) | Free | Medium | Varies | Complex |

## Next Steps

Once configured:
1. ✅ Test connection: `uv run python backend/test_llm_connection.py`
2. ✅ Test characters: `uv run python backend/test_character_live.py`
3. ✅ Start server: `uv run python backend/main.py`
4. ✅ Build frontend integration

## Support

- Anthropic docs: https://docs.anthropic.com/
- OpenAI docs: https://platform.openai.com/docs
- Ollama docs: https://github.com/ollama/ollama
- Character system docs: `backend/CHARACTER_SYSTEM_README.md`
