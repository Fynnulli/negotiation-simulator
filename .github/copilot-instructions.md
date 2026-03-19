# Negotiation Simulator — Project Instructions

## Overview

This is a local Python-based prototype for AI-supported negotiation preparation. The system simulates negotiation scenarios with different opponent agents (cooperative, hardball, skeptical, analytical) and provides structured feedback on negotiation performance.

## Key Principles

1. **Modular Design**: Each agent has isolated behavior definition; scenarios are composable
2. **Prompt-Driven**: Agent behavior emerges from markdown-based agent definitions, not code hardcoding
3. **Structured Feedback**: Reflection output follows predictable templates for analysis and learning
4. **Minimal Dependencies**: Core functionality uses standard Python libraries only
5. **Documentation-First**: All agent behavior lives in readable markdown before implementation

## Code Organization

- `app.py` — Main entry point / simulation orchestrator
- `utils/` — Reusable functions (LLM client, prompt loading, simulation runner)
- `agents/` — Agent behavior definitions (markdown files)
- `prompts/` — Prompt templates for scenario building and feedback
- `data/` — Sample negotiation cases and test data

## When to Use Agents

- **planner**: Break down a multi-step implementation task
- **builder**: Execute a specific implementation task
- **Explore**: Quick codebase questions and exploration

## Implementation Standards

- Follow [python.instructions.md](../python.instructions.md) for code style
- Follow [agents.instructions.md](../agents.instructions.md) for creating agent definitions
- Validate all YAML frontmatter in agent and prompt files
- Keep agent definitions concise and behaviorally explicit
