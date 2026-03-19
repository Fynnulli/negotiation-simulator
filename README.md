# Negotiation Simulator

A local, AI-powered prototype for negotiation preparation and practice. Practice your negotiation skills against different opponent agents (cooperative, hardball, skeptical, analytical) and receive structured feedback on your approach.

## Features

- 🤝 **Multiple Opponent Types**: Cooperative (win-win), Hardball (aggressive), Skeptical (cautious), Analytical (data-driven)
- 💬 **Single-Turn Simulation**: Make an opening proposal, receive response, get feedback
- 📊 **Structured Scenario Building**: Convert your negotiation context into a clear scenario
- 📈 **Intelligent Feedback**: Post-simulation reflection on strategy, communication, and outcomes
- 🔧 **Markdown-Based Agent Definitions**: Easy to understand and modify agent behavior
- 🚀 **Streamlit UI**: Simple, interactive web interface
- 🔐 **Local Only**: All computation happens locally with your API keys

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

### Running the Simulator

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

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

## Customization

### Modifying Agent Behavior

Edit the Markdown files in `agents/`:
- `opponent_cooperative.md`, `opponent_hardball.md`, etc.
- Change role, tone, objectives, constraints, or behavior guidelines
- The simulator will use the updated behavior on next run

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
- Check that `.env` exists
- Verify `OPENAI_API_KEY` is set and valid
- Test your key at https://platform.openai.com/

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
