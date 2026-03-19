---
name: "bootstrap-negotiation-prototype"
description: "Entry point to create a negotiation scenario and begin simulation"
---

# Bootstrap Negotiation Prototype

## Overview

This prompt initiates a new negotiation simulation. It gathers scenario details from the user and sets up a negotiation with a selected opponent type.

## Workflow

1. **Scenario Creation**: Collect negotiation context (topic, goals, constraints)
2. **Opponent Selection**: Choose which opponent type to simulate (cooperative, hardball, skeptical, analytical)
3. **Scenario Formatting**: Convert user input into structured negotiation scenario using `prompts/scenario_builder.md`
4. **Simulation Setup**: Initialize the negotiation with the selected opponent
5. **Negotiation Rounds**: Run multi-turn conversation between user and opponent
6. **Reflection**: Analyze the completed negotiation using `prompts/feedback_template.md`

## Input Requirements

The simulation needs:
- **Scenario Topic**: What are you negotiating? (e.g., salary, contract terms, partnership)
- **Your Goal**: What do you want to achieve?
- **Your Constraints**: What are your walkaway positions and non-negotiables?
- **Opponent Type**: Which agent should oppose you?
  - `cooperative` — Win-win focused
  - `hardball` — Aggressive, self-interested
  - `skeptical` — Doubtful, needs proof
  - `analytical` — Data-driven, methodical

## Output

- Initialized negotiation between user and opponent
- Multi-turn conversation structure
- Post-simulation reflection and feedback

## Example Invocation

```
Create a negotiation scenario:
Topic: Business partnership proposal
My goal: Establish 50/50 partnership with existing contacts
Constraints: Must retain creative control, willing to compromise on equity split
Opponent type: analytical
```
