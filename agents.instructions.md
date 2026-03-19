# Agent Definition Standards

## Overview

Negotiation agents are defined using markdown files with YAML-based configuration. Each agent has a clear role, tone, and set of behaviors that guide its responses during negotiation simulation.

## Agent File Structure

Every agent markdown file should follow this structure:

```
---
role: "Agent role/title"
tone: "Communication style: warm, direct, skeptical, analytical, etc."
objectives: ["Primary goal 1", "Secondary goal 2"]
constraints: ["Constraint 1", "Constraint 2"]
---

## Role Description

Brief 1-2 sentence description of the agent's purpose and position.

## Behavior Guidelines

- **Opening**: How to approach early negotiation phase
- **In Negotiation**: How to respond to offers and counteroposals
- **Closing**: How to finalize or walk away
- **Handling Objections**: Standard response pattern

## Example Interaction

[Optional: Example dialogue or scenario]
```

## Opponent Agent Types

Four standard opponent types are defined:

1. **Cooperative**: Open-minded, seeks win-win, transparent
2. **Hardball**: Aggressive, demands value, minimal concessions
3. **Skeptical**: Doubtful, needs proof, slow to commit
4. **Analytical**: Data-driven, methodical, detail-focused

## Reflection Agent

The reflection agent analyzes a complete negotiation and produces structured feedback without participating in the negotiation itself.

## Guidelines

- Keep tone descriptions concrete and observable (avoid vague terms)
- Objectives should be measurable or clear outcomes
- Constraints prevent unrealistic behavior (e.g., "will not agree below X baseline")
- Behavior guidelines should be reusable by both humans and LLM implementations
- Use bullet points for scannability

## YAML Frontmatter Rules

- Quote all string values containing colons
- Use YAML arrays for lists (`["item1", "item2"]`)
- Keep the frontmatter section compact (≤10 lines)
- Never use tabs; use 2 spaces for indentation
