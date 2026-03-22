# Copilot Task: Replace Streamlit Interface with Claude-Native Interface

## Context

This project is a negotiation simulator. The current architecture uses
Streamlit (app.py) as the UI layer. We are replacing this with a
Claude.ai Project-based interface using a system prompt file.

The negotiation logic (agents, prompts, simulator, llm_client) stays
completely unchanged. Only the interface layer changes.

---

## What to DELETE

Remove the following file entirely:
- `app.py`

---

## What to ADD

Create a new file at the project root: `claude_interface.md`

Paste the full content of the file I provide below into it. Do not
modify the content — copy it exactly.

[PASTE CONTENT OF claude_interface.md HERE]

---

## What to UPDATE

### 1. README.md

Replace the "Running the Simulator" section with:

```markdown
## Two Ways to Use the Simulator

### Option A — Claude.ai Project (Recommended)
1. Open [claude.ai/projects](https://claude.ai/projects)
2. Create a new Project
3. Paste the full content of `claude_interface.md` as the Project
   System Prompt
4. Start chatting — type `START` to begin a simulation

No API key, no terminal, no hosting required.

### Option B — Local Streamlit (Legacy)
If you want to run the original Streamlit interface locally:
```bash
streamlit run app_legacy.py
```
(Requires API key in `.env`)
```

### 2. Rename app.py → app_legacy.py

Do not delete app.py — rename it to app_legacy.py so the Streamlit
option still works locally if needed.

### 3. Update .gitignore

Add this line at the bottom:
```
# Legacy UI
app_legacy.py
```

---

## What NOT to change

Do not touch any of the following:
- `utils/simulator.py`
- `utils/prompt_loader.py`
- `utils/llm_client.py`
- `agents/*.md`
- `prompts/*.md`
- `requirements.txt`
- `.env.example`

---

## Summary of Changes

| File | Action |
|------|--------|
| `app.py` | Rename to `app_legacy.py` |
| `claude_interface.md` | CREATE (new primary interface) |
| `README.md` | Update "Running" section |
| `.gitignore` | Add `app_legacy.py` entry |

---

## Verification

After making changes, confirm:
- [ ] `claude_interface.md` exists at project root
- [ ] `app.py` is renamed to `app_legacy.py`
- [ ] README describes both options
- [ ] No Python logic was modified
