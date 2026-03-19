---
name: "scenario_builder"
description: "Transforms raw negotiation input into structured scenario definition"
---

# Scenario Builder Prompt

## Purpose

Convert user-provided negotiation context into a structured, LLM-readable scenario that both human negotiators and AI agents can understand clearly.

## Input Format

```
Topic: [negotiation subject]
Your Goal: [primary objective]
Your Baseline: [minimum acceptable outcome]
Constraints/Non-Negotiables: [lines you won't cross]
Background/Context: [relevant history or external factors]
```

## Output Format

```json
{
  "scenario": {
    "topic": "string",
    "context": "string",
    "your_position": {
      "primary_goal": "string",
      "baseline_acceptable": "string",
      "walkaway_position": "string",
      "non_negotiables": ["item1", "item2"],
      "flexibility_areas": ["area1", "area2"]
    },
    "opponent_profile": {
      "type": "cooperative|hardball|skeptical|analytical",
      "likely_interests": ["interest1", "interest2"],
      "likely_constraints": ["constraint1", "constraint2"]
    },
    "success_metrics": [
      "metric1 (quantitative or observable)",
      "metric2"
    ]
  }
}
```

## Transformation Rules

1. **Clarify Ambiguity**: If user says "fair deal," ask what that means quantitatively
2. **Identify Trade-offs**: Map areas where you can compromise vs. where you cannot
3. **Infer Opponent Profile**: Based on context, suggest opponent type and likely positions
4. **Define Success**: Make vague goals measurable (e.g., "good outcome" → "10% reduction in price")
5. **Validate Walkaway**: Ensure walkaway position is realistic and defined quantitatively

## Example Transformation

**Input:**
```
Topic: Freelance contract terms
Your Goal: $50/hour with benefits
Constraints: Must be able to work remotely
```

**Output:**
```json
{
  "scenario": {
    "topic": "Freelance contract rate and flexibility terms",
    "context": "Negotiating first long-term freelance engagement",
    "your_position": {
      "primary_goal": "$50/hour with health insurance stipend",
      "baseline_acceptable": "$45/hour + 50% health coverage",
      "walkaway_position": "$40/hour with full remote flexibility",
      "non_negotiables": ["100% remote work", "flexible hours"],
      "flexibility_areas": ["rate", "benefits structure", "contract length"]
    },
    "opponent_profile": {
      "type": "analytical",
      "likely_interests": ["cost control", "clear deliverables", "predictable productivity"],
      "likely_constraints": ["budget limits", "hiring approval process"]
    },
    "success_metrics": [
      "Hourly rate matches or exceeds $45/hour",
      "100% remote work clause included",
      "Health insurance component worth ≥$150/month",
      "Agreement signed within 2 meetings"
    ]
  }
}
```
