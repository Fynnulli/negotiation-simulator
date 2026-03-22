# Negotiation Simulator

A local, AI-powered prototype for negotiation preparation and practice. Practice your negotiation skills against different opponent agents (cooperative, hardball, skeptical, analytical) and receive structured feedback on your approach.

## Features

- 🔌 **Multiple LLM Providers**: Support for OpenAI (GPT-4), Anthropic (Claude), and Google (Gemini)

## Setup

### Prerequisites

- Python 3.10+
- OpenAI API key (for GPT-4)

### Installation

1. **Clone or download the project**
   ```bash
   cd negotiation-simulator
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your API key**
   - Rename `.env.example` to `.env`
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=sk-your-key-here
     OPENAI_MODEL=gpt-4
     ```

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

## Usage

### Basic Workflow

1. **Set Up Your Scenario**
   - Describe the negotiation topic
   - State your goal and minimum acceptable baseline
   - Provide your BATNA (walkaway position)
   - Describe the counterparty
   - Add any relevant context

2. **Choose an Opponent**
   - **Cooperative**: Seeks win-win solutions, transparent, collaborative
   - **Hardball**: Aggressive, pushes for maximum gains, competitive
   - **Skeptical**: Cautious, needs proof, risk-averse
   - **Analytical**: Data-driven, logical, detail-focused

3. **Make Your Opening Offer**
   - Write your opening statement or proposal
   - Click "Run Simulation"

4. **Review Results**
   - See the structured scenario
   - Read the opponent's response
   - Get feedback on your approach, communication, strategy, and outcomes

### Example Scenario

**Topic**: Freelance Project Rate  
**Goal**: $60/hour with project flexibility  
**Baseline**: $50/hour  
**BATNA**: Stay in current role (less interesting work)  
**Counterparty**: Growing startup, budget-aware, need experienced frontend dev  

**Opening**: "I'm excited about this project. Based on my experience with React and the project scope you mentioned, my rate is $60/hour. I can also offer flexible hours since our timezones align."

## Project Structure

```
negotiation-simulator/
├── agents/                           # Opponent agent definitions (Markdown)
│   ├── opponent_cooperative.md
│   ├── opponent_hardball.md
│   ├── opponent_skeptical.md
│   ├── opponent_analytical.md
│   └── reflection_agent.md
│
├── prompts/                          # Prompt templates (Markdown)
│   ├── scenario_builder.md          # Formats user input into scenario
│   └── feedback_template.md         # Feedback structure for reflection
│
├── utils/                            # Python utilities
│   ├── prompt_loader.py             # Load & parse Markdown files
│   ├── llm_client.py                # OpenAI API abstraction
│   └── simulator.py                 # Negotiation orchestration
│
├── app.py                            # Streamlit UI
├── requirements.txt                  # Python dependencies
├── .env.example                      # API key template
└── README.md                         # This file
```

## Architecture

### Data Flow

```
User Input
    ↓
scenario_builder.md (Prompt)
    ↓
Structured Scenario
    ↓
Opponent Agent (Markdown) + Negotiation Prompt
    ↓
LLM API Call
    ↓
Opponent Response
    ↓
Reflection Agent + Feedback Template
    ↓
Structured Feedback
    ↓
Streamlit UI Display
```

### Key Components

- **prompt_loader.py**: Parses YAML frontmatter from Markdown files, loads agent behavior definitions
- **llm_client.py**: Simple OpenAI wrapper, environment-based configuration, easy to swap providers
- **simulator.py**: Orchestrates scenario building, negotiation simulation, and reflection
- **app.py**: Streamlit UI with input form and multi-tab result display

## Configuration

### Environment Variables

Create a `.env` file (copy from `.env.example`):

```env
OPENAI_API_KEY=sk-...                # Your OpenAI API key (required)
OPENAI_MODEL=gpt-4                   # Model to use (default: gpt-4)
OPENAI_TEMPERATURE=0.7               # Sampling temperature (0.0-1.0)
STREAMLIT_SERVER_PORT=8501           # Streamlit port (optional)
```
Create a `.env` file (copy from `.env.example`):

```env
# Select which provider to use (default: openai)
LLM_PROVIDER=openai  # Options: openai, claude, gemini

# OpenAI (GPT-4)
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4

# Anthropic Claude
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-3-opus-20240229

# Google Gemini
GOOGLE_API_KEY=your-key-here
GOOGLE_MODEL=gemini-pro

# Optional
OPENAI_TEMPERATURE=0.7
STREAMLIT_SERVER_PORT=8501
```

### Supported LLM Providers

The simulator supports three major LLM providers:

#### OpenAI (GPT-4)
- **Model**: `gpt-4` (or `gpt-3.5-turbo` for faster, lower-cost option)
- **Setup**: Get API key from https://platform.openai.com/api-keys
- **Set in .env**: `LLM_PROVIDER=openai`

#### Anthropic (Claude)
- **Model**: `claude-3-opus-20240229` (highest-performance), `claude-3-sonnet-20240229` (balanced), `claude-3-haiku-20240307` (fast)
- **Setup**: Get API key from https://console.anthropic.com/
- **Set in .env**: `LLM_PROVIDER=claude`

#### Google (Gemini)
- **Model**: `gemini-pro` (recommended)
- **Setup**: Get API key from https://makersuite.google.com/app/apikey
- **Set in .env**: `LLM_PROVIDER=gemini`
## Customization

### Modifying Agent Behavior

Edit the Markdown files in `agents/`:
- `opponent_cooperative.md`, `opponent_hardball.md`, etc.
- Change role, tone, objectives, constraints, or behavior guidelines
- The simulator will use the updated behavior on next run

### Switching LLM Providers

**Option 1: Environment Variable (Recommended)**
Edit `.env` and change `LLM_PROVIDER`:
```env
LLM_PROVIDER=claude  # Switch to Claude
# OR
LLM_PROVIDER=gemini  # Switch to Gemini
```

**Option 2: UI Selection**
The Streamlit app sidebar includes a dropdown to select the LLM provider on-the-fly without restarting.

**Feature Comparison**:
| Provider | Speed | Cost | Quality | Best For |
|----------|-------|------|---------|----------|
| OpenAI (GPT-4) | Medium | Higher | Excellent | General purpose, proven |
| Claude | Medium | Medium | Excellent | Long context, nuanced responses |
| Gemini | Fast | Lower | Good | Quick iterations, cost-conscious |
### Creating a New Agent Type

1. Create `agents/opponent_<name>.md` with YAML frontmatter:
   ```yaml
   ---
   role: "Your Agent Name"
   tone: "Your description"
   objectives: ["Goal 1", "Goal 2"]
   constraints: ["Constraint 1"]
   ---
   ```
2. The agent will automatically appear in the opponent selection dropdown

## Limitations & Notes

- **Single-turn**: Current version allows one opening + one response. Multi-turn support is future work.
- **Model-dependent**: Output quality depends on your OpenAI model choice (GPT-4 recommended).
- **Local execution**: Requires valid OpenAI API credentials and internet connection.
- **No persistence**: Results are not saved between sessions; you can copy/paste feedback.

## Future Enhancements

- [ ] Multi-turn negotiation support
- [ ] Conversation history and replay
- [ ] Custom scenario templates
- [ ] Performance metrics tracking
- [ ] Export results to PDF
- [ ] Support for other LLM providers (Anthropic, local models)

## Troubleshooting

### "Missing directory: agents"
Ensure you're running the app from the project root directory.

### "API Configuration Error"
@@Check that `.env` exists
@@Verify the selected LLM_PROVIDER has a valid API key configured
### "API Configuration Error"
- Check that `.env` exists
- Verify `OPENAI_API_KEY` is set and valid
- Test your key at https://platform.openai.com/

### Provider-Specific Issues

**OpenAI**: Verify key at https://platform.openai.com/api-keys/keys  
**Claude**: Verify key at https://console.anthropic.com/  
**Gemini**: Verify key at https://makersuite.google.com/app/apikey

### "Module not found" errors
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again

### Streamlit errors
- Clear Streamlit cache: `streamlit cache clear`
- Restart the app: `streamlit run app.py`

## Development

For development, install additional tools:
```bash
pip install pytest black flake8 mypy
```

## License

Local prototype for educational and personal use.

## Support

For issues or questions:
1. Check the project structure matches the expected layout
2. Review `.env` configuration
3. Test the OpenAI API key independently
4. Check log output in the terminal running `streamlit run app.py`
