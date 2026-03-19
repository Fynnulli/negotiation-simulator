# Python Development Standards

## Code Style

- **PEP 8 compliance**: Follow standard Python naming (snake_case for functions/variables, PascalCase for classes)
- **Type hints**: Add type annotations to all function signatures
- **Docstrings**: Use Google-style docstrings for all public functions and classes
- **Line length**: Keep lines ≤100 characters
- **Imports**: Use explicit imports; order as stdlib, third-party, local (separated by blank lines)

## Project Structure

```
utils/
├── llm_client.py      # OpenAI/LLM client wrapper
├── prompt_loader.py   # Load and format markdown prompts
└── simulator.py       # Core negotiation simulation logic
```

## Dependencies

- Dependencies go in `requirements.txt`
- Use semantic versioning constraints (e.g., `requests>=2.28.0,<3.0`)
- Minimal core dependencies; suggest optional extras for advanced features

## Testing & Validation

- Create test cases in a future `tests/` directory
- Validate prompt loading before runtime
- Log agent interactions for debugging/feedback analysis

## Error Handling

- Catch and handle LLM API failures gracefully
- Provide clear, actionable error messages
- Log failures without exposing API keys

## Constants & Configuration

- Environment variables via `.env` (use `.env.example` as template)
- Configuration classes for complex settings
- Avoid magic numbers; use named constants
