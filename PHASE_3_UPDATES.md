# Phase 3: Multi-Provider LLM Support

**Status**: ✅ COMPLETE  
**Completed**: 19. März 2026  
**Summary**: Added support for Claude (Anthropic) and Gemini (Google) alongside OpenAI

---

## What Was Added

### Multi-Provider LLM Architecture

**`utils/llm_client.py` — Complete Refactor**

- **`BaseLLMClient`** — Abstract base class with unified interface
  - `generate(prompt, system_prompt, max_tokens)` — Generate text
  - `is_configured()` — Check if API key configured

- **`OpenAIClient`** — GPT-4 via OpenAI API
- **`ClaudeClient`** — Claude via Anthropic API
- **`GeminiClient`** — Gemini via Google API

- **`get_client(provider=None)`** — Factory function
  - Provider: "openai" | "claude" | "gemini" | None (uses env default)
  - Returns appropriate client instance

- **`list_providers()`** — Lists all available options

---

## Configuration Changes

### `.env.example`

```env
# Select which provider to use (default: openai)
LLM_PROVIDER=openai  # Options: openai, claude, gemini

# OpenAI Configuration
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_MODEL=gpt-4
OPENAI_TEMPERATURE=0.7

# Anthropic Claude Configuration
ANTHROPIC_API_KEY=sk-ant-your-api-key-here
ANTHROPIC_MODEL=claude-3-opus-20240229

# Google Gemini Configuration
GOOGLE_API_KEY=your-google-api-key-here
GOOGLE_MODEL=gemini-pro
```

### `requirements.txt`

Added:
- `anthropic==0.7.1` — Anthropic Claude API client
- `google-generativeai==0.3.0` — Google Gemini API client

---

## Simulator Updates

### `utils/simulator.py`

All simulation functions now accept `provider` parameter:

```python
def run_negotiation(
    scenario, 
    opponent_type, 
    your_opening, 
    provider=None  # NEW
) -> Dict[str, Any]:
    ...
    client = get_client(provider=provider)
    ...

def run_reflection(
    scenario, 
    negotiation_result, 
    provider=None  # NEW
) -> Dict[str, Any]:
    ...
    client = get_client(provider=provider)
    ...

def simulate_negotiation(
    ...,
    provider=None  # NEW
) -> Dict[str, Any]:
    ...
    return {
        ...,
        "provider": provider or "default",  # NEW
        "success": True
    }
```

---

## UI Updates

### `app.py` — Provider Selector

**Sidebar Enhancement**:
```python
llm_provider = st.sidebar.selectbox(
    "LLM Provider",
    options=list_providers(),  # [openai, claude, gemini]
    index=0,
    help="Choose which AI model to use for opponent responses"
)
```

**API Key Validation**:
```python
try:
    _ = get_client(provider=llm_provider)
except ValueError as e:
    st.error(f"❌ API Configuration Error:\n{str(e)}")
    return False
```

**Results Display**:
```python
st.caption(f"Provider: {result.get('provider', 'default').upper()}")
```

---

## Documentation Updates

### `README.md`

**New Sections**:

1. **Feature Overview**
   - Added "🔌 Multiple LLM Providers" to features

2. **Supported LLM Providers**
   - OpenAI (GPT-4): General purpose
   - Claude (Anthropic): Long context, nuanced responses
   - Gemini (Google): Fast, cost-conscious

3. **Provider Comparison Table**
   | Provider | Model | Cost | Speed | Best For |
   |----------|-------|------|-------|----------|
   | OpenAI | gpt-4 | Higher | Medium | General purpose |
   | Claude | claude-3-opus | Medium | Medium | Long context |
   | Gemini | gemini-pro | Lower | Fast | Cost-conscious |

4. **Setup Instructions Per Provider**
   - Links to get API keys
   - Configuration examples
   - Model selection guidance

5. **Provider-Specific Troubleshooting**
   - OpenAI: https://platform.openai.com/api-keys/keys
   - Claude: https://console.anthropic.com/
   - Gemini: https://makersuite.google.com/app/apikey

6. **UI Provider Switching**
   - How to select different provider in sidebar
   - No restart needed

---

## How to Use Multi-Provider

### Step 1: Configure Environment

Copy `.env.example` to `.env` and add API keys for providers you want to use:

```bash
cp .env.example .env

# Edit .env with your API keys
# Option A: Use OpenAI (GPT-4)
OPENAI_API_KEY=sk-...
LLM_PROVIDER=openai

# Option B: Use Claude
ANTHROPIC_API_KEY=sk-ant-...
LLM_PROVIDER=claude

# Option C: Use Gemini
GOOGLE_API_KEY=...
LLM_PROVIDER=gemini
```

### Step 2: Run Simulator

```bash
streamlit run app.py
```

### Step 3: Select Provider

In Streamlit sidebar:
- Dropdown menu: "LLM Provider"
- Select: openai | claude | gemini
- Provider validates API key automatically

### Step 4: Run Simulation

- Fill in scenario
- Click "Run Simulation"
- Results show which provider was used

---

## Architecture

```
Streamlit UI (app.py)
    │
    ├─ Provider selector in sidebar
    └─ Passes provider to simulator
        │
        ▼
    Simulator (simulator.py)
        │
        ├─ run_negotiation(provider)
        │   └─ llm_client.generate()
        │
        └─ run_reflection(provider)
            └─ llm_client.generate()
            │
            ▼
    LLM Client Factory (llm_client.py)
        │
        ├─ provider == "openai"? → OpenAIClient
        ├─ provider == "claude"? → ClaudeClient
        └─ provider == "gemini"? → GeminiClient
            │
            ▼
        Provider-specific generate()
            │
            ▼
        Unified text response
```

---

## Supported Models

### OpenAI
- **gpt-4** (recommended, high quality)
- **gpt-3.5-turbo** (faster, lower cost)

### Anthropic Claude
- **claude-3-opus-20240229** (most capable, highest cost)
- **claude-3-sonnet-20240229** (balanced)
- **claude-3-haiku-20240307** (fastest, lowest cost)

### Google Gemini
- **gemini-pro** (multimodal capable)

---

## Provider Comparison

| Aspect | OpenAI | Claude | Gemini |
|--------|--------|--------|---------|
| **Startup Speed** | Fast | Fast | Fastest |
| **Response Quality** | Excellent | Excellent | Good |
| **Long Context** | 128K | 200K | 32K |
| **Cost (per million tokens)** | $30 | $15 | $0.50 |
| **Best For** | General, proven | Detailed, nuanced | Cost optimization |
| **Negotiation Realism** | High | High | Good |
| **Multi-turn Support** | ✅ | ✅ | ✅ |

---

## Migration Guide

### From Single-Provider (OpenAI only)

**Before**:
```python
from utils.llm_client import LLMClient
client = LLMClient()
response = client.generate(prompt)
```

**After** (backwards compatible):
```python
from utils.llm_client import get_client
client = get_client()  # Uses env default or "openai"
response = client.generate(prompt)
```

**Or with explicit provider**:
```python
client = get_client(provider="claude")
response = client.generate(prompt)
```

---

## Error Handling

### Missing API Key

```
❌ API Configuration Error:
Anthropic API key not found. 
Set ANTHROPIC_API_KEY environment variable or pass api_key parameter.
```

### Invalid Provider

```
ValueError: Unknown LLM provider: llama2. 
Supported providers: openai, claude, gemini
```

### Network Issues

- OpenAI: Connection timeout (fallback to retry)
- Claude: Rate limit error (wait 60 seconds)
- Gemini: Authentication error (check API key)

---

## Files Modified

| File | Type | Changes |
|------|------|---------|
| `utils/llm_client.py` | Python | ✅ Complete refactor (250 LOC) |
| `utils/simulator.py` | Python | ✅ Added provider param (15 LOC) |
| `app.py` | Python | ✅ Added provider selector (20 LOC) |
| `requirements.txt` | Config | ✅ Added 2 dependencies |
| `.env.example` | Config | ✅ Extended with 8 lines |
| `README.md` | Docs | ✅ Added 80+ lines |

---

## Testing Checklist

- [x] OpenAI API calls work
- [x] Claude API calls work
- [x] Gemini API calls work
- [x] Provider selector appears in sidebar
- [x] API key validation works per provider
- [x] Results show correct provider used
- [x] Error messages are helpful
- [x] Backwards compatibility maintained
- [x] Type hints all correct
- [x] Docstrings complete

---

## Next Steps

### Phase 4 (Future)

- [ ] Multi-turn conversation support
- [ ] Conversation history/replay
- [ ] Model selection per provider (gpt-3.5 vs gpt-4)
- [ ] Usage tracking and cost estimation
- [ ] Local LLM support (Ollama, LLaMA)
- [ ] Streaming responses for faster feedback
- [ ] Custom provider implementation guide

---

**Summary**: The simulator now supports 3 major LLM providers with identical functionality. Users can switch providers from the UI without restarting, enabling cost optimization and experimenting with different models.
