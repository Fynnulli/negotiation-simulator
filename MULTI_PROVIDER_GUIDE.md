# Multi-Provider LLM Support — Quick Reference

## What's New  ✨

Your Negotiation Simulator now supports **3 major LLM providers**:

1. **🔵 OpenAI** — GPT-4 (default)
2. **🤖 Anthropic** — Claude (new)
3. **🔎 Google** — Gemini (new)

Switch between them instantly from the Streamlit UI **without restarting the app**.

---

## Quick Start

### 1. Install New Dependencies
```bash
pip install -r requirements.txt
```

This already includes:
- `anthropic==0.7.1` 
- `google-generativeai==0.3.0`

### 2. Configure API Keys

```bash
cp .env.example .env
```

Add your API keys to `.env`:

```env
# Choose your default provider
LLM_PROVIDER=openai  # or claude, or gemini

# If using OpenAI:
OPENAI_API_KEY=sk-...

# If using Claude:
ANTHROPIC_API_KEY=sk-ant-...

# If using Gemini:
GOOGLE_API_KEY=...
```

### 3. Run the App
```bash
streamlit run app.py
```

### 4. Select Provider in Sidebar
A new dropdown in the sidebar lets you pick which provider to use:

```
⚙️ Configuration
├─ Opponent Type: [cooperative ▼]
├─ LLM Provider:  [openai ▼]  ← NEW!
│                 • openai
│                 • claude
│                 • gemini
```

---

## Provider API Keys

| Provider | Where to Get | Cost Tier |
|----------|-------------|-----------|
| **OpenAI** | https://platform.openai.com/api-keys | Free trial, then pay per token |
| **Claude** | https://console.anthropic.com/ | Free trial available |
| **Gemini** | https://makersuite.google.com/app/apikey | Free tier available |

---

## Which Provider Should I Use?

### OpenAI (Default) ✅
- **Best for**: General purpose, proven track record
- **Speed**: Medium (~5 seconds per response)
- **Quality**: Excellent negotiation responses
- **Cost**: ~$0.01-0.05 per simulation
- **Model**: gpt-4 (or gpt-3.5-turbo for faster/cheaper)

### Claude 🤖
- **Best for**: Long contexts, nuanced responses, detailed feedback
- **Speed**: Medium (~4 seconds per response)
- **Quality**: Excellent, very natural language
- **Cost**: ~$0.01-0.03 per simulation
- **Model**: claude-3-opus-20240229

### Gemini 🔎
- **Best for**: Cost-conscious, quick iterations
- **Speed**: Fast (~2 seconds per response)
- **Quality**: Good, somewhat shorter responses
- **Cost**: ~$0.001 per simulation (cheapest)
- **Model**: gemini-pro

---

## Usage Examples

### Via Environment Variable
Set default provider in `.env`:
```env
LLM_PROVIDER=claude
ANTHROPIC_API_KEY=sk-ant-...
```

Then run: `streamlit run app.py`

Every simulation uses Claude by default.

### Via Streamlit UI
1. Run `streamlit run app.py`
2. Click dropdown in sidebar: `LLM Provider`
3. Select `claude` or `gemini`
4. Fill form and run simulation
5. Claude/Gemini is used for this simulation

Switch between providers without restarting!

---

## What Changed in the Code

### `utils/llm_client.py`
- ✅ Created `BaseLLMClient` abstract class
- ✅ Implemented `OpenAIClient`, `ClaudeClient`, `GeminiClient`
- ✅ Factory function: `get_client(provider="openai")`
- ✅ All return unified text response

### `utils/simulator.py`
- ✅ Added `provider=None` parameter to:
  - `run_negotiation(..., provider)`
  - `run_reflection(..., provider)`
  - `simulate_negotiation(..., provider)`

### `app.py` (Streamlit)
- ✅ Added provider dropdown in sidebar
- ✅ Validates API key for selected provider
- ✅ Passes provider to simulator
- ✅ Shows provider in results

### Configuration
- ✅ `requirements.txt` — Added anthropic, google-generativeai
- ✅ `.env.example` — Added ANTHROPIC & GOOGLE config

### Documentation
- ✅ `README.md` — Provider setup & comparison
- ✅ `PHASE_3_UPDATES.md` — Detailed Phase 3 documentation

---

## Examples: Same Scenario, Different Providers

### **Scenario**: Freelance rate negotiation
**Your Opening**: "My rate is $60/hour with health insurance coverage."

### OpenAI Response (GPT-4):
> "I appreciate your experience, but we have a budget framework. Your rate is above our range of $45-55/hour. However, I'm interested in discussing whether you'd consider a project-based rate or retainer with fewer hours..."

### Claude Response (claude-3-opus):
> "Thank you for the proposal. I understand the value you bring to the table. However, I need to be transparent that our current budget allocation doesn't accommodate the $60/hour rate. Could we explore alternative structures? For instance, would you be open to a slightly lower hourly rate in exchange for guaranteed monthly hours..."

### Gemini Response (gemini-pro):
> "I see your rate. That's higher than our budget. Can you do $50/hour? We have other requirements too that might help. What features are most important to you?"

---

## Troubleshooting

### "API Configuration Error"

**Error**: Provider selected but API key not configured

**Solution**: 
1. Check `.env` file has the right API key for selected provider
2. Make sure you copied `.env.example` to `.env` first
3. Verify API key is valid (test on provider's website)

**Example**:
```env
LLM_PROVIDER=claude
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here  ← Not placeholder!
```

### "Module not found: anthropic"

**Solution**: Reinstall dependencies
```bash
pip install -r requirements.txt
```

### "Model not found"

**Solution**: Check correct model name in `.env`
```env
ANTHROPIC_MODEL=claude-3-opus-20240229  # ✅ Correct
ANTHROPIC_MODEL=claude-3  # ❌ Wrong
```

---

## Cost Estimates Per Simulation

(Approximate, based on ~2000 input tokens, ~500 output tokens)

| Provider | Cost per Sim | 100 Sims |
|----------|-------------|----------|
| OpenAI (gpt-4) | ~$0.04 | ~$4 |
| Claude (opus) | ~$0.02 | ~$2 |
| Gemini (pro) | ~$0.001 | ~$0.10 |

---

## Advanced: Custom Provider

Want to add support for another LLM (Llama 2, Mistral, etc.)?

```python
# In utils/llm_client.py

class LlamaClient(BaseLLMClient):
    def __init__(self, api_key, model):
        self.client = # initialize your Llama API
    
    def generate(self, prompt, system_prompt=None, max_tokens=1500):
        # Call your Llama API
        return response_text
    
    def is_configured(self):
        return bool(self.api_key)

# In get_client() factory:
    elif provider == "llama":
        return LlamaClient(...)
```

Then update `.env.example` and add to `list_providers()`.

---

## Files Updated

```
negotiation-simulator/
├── utils/
│   ├── llm_client.py         ✅ Refactored (250 LOC)
│   └── simulator.py          ✅ Added provider param
├── app.py                     ✅ Added provider selector
├── requirements.txt           ✅ +2 dependencies
├── .env.example              ✅ Extended config
├── README.md                 ✅ Provider docs
└── PHASE_3_UPDATES.md        ✅ Complete Phase 3 docs
```

---

**Next**: Open `PHASE_3_UPDATES.md` for detailed technical documentation, or just start using different providers! 🚀
