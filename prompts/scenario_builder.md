---
name: "scenario_builder"
description: "Transforms raw negotiation input into a structured scenario
  grounded in Lewicki et al. (2010) planning steps 1–8"
---

# Scenario Builder Prompt

## Purpose

Convert user-provided negotiation context into a structured,
LLM-readable scenario. The output maps directly onto the ten
planning steps of Lewicki et al. (2010, S. 119 ff.) and
distinguishes between distributive and integrative negotiation
contexts (Lewicki et al., 2010, S. 46 ff.).

---

## Theoretical Mapping

| Output field            | Lewicki planning step         |
|-------------------------|-------------------------------|
| `topic`                 | Step 1 — Defining the Issues  |
| `bargaining_mix`        | Step 2 — Assembling the Bargaining Mix |
| `interests`             | Step 3 — Defining Interests   |
| `resistance_point`      | Step 4 — Defining Resistance Points |
| `batna`                 | Step 5 — Defining Alternatives (BATNA) |
| `target` / `opening`   | Step 6 — Defining Targets and Opening Bids |
| `context`               | Step 7 — Assessing Social Context |
| `opponent_profile`      | Step 8 — Analyzing the Other Party |

---

## Input Format

```
Topic:            [what is being negotiated]
Your Goal:        [primary objective — target point]
Your Baseline:    [minimum acceptable — resistance point]
BATNA:            [best alternative if no deal]
Constraints:      [non-negotiables]
Counterparty:     [who / what organization]
Context / Tone:   [relationship history, cultural factors, setting]
```

---

## Output Format

```json
{
  "scenario": {
    "topic": "string",
    "negotiation_type": "distributive | integrative | mixed",
    "negotiation_type_rationale": "string — why this classification",

    "your_position": {
      "target_point": "string",
      "resistance_point": "string — minimum acceptable outcome",
      "batna": "string — walkaway alternative",
      "non_negotiables": ["item1", "item2"],
      "flexibility_areas": ["area1", "area2"]
    },

    "bargaining_mix": [
      {
        "issue": "string",
        "priority": "high | medium | low",
        "linked_to": "string or null — issue it is connected to",
        "type": "tangible | intangible"
      }
    ],

    "interests": {
      "substantive": ["direct outcome interests"],
      "process": ["interests related to how negotiation unfolds"],
      "relational": ["interests tied to relationship with other party"]
    },

    "opponent_profile": {
      "type": "cooperative | hardball | skeptical | analytical",
      "likely_batna": "string — estimated alternative",
      "likely_interests": ["interest1", "interest2"],
      "likely_resistance_point": "string — estimated walkaway",
      "likely_strategy": "distributive | integrative | mixed"
    },

    "success_metrics": [
      "metric1 — quantitative or clearly observable",
      "metric2"
    ]
  }
}
```

---

## Classification Rules

**Distributive** — apply when:
- Single issue (e.g., price only)
- No ongoing relationship expected
- Zero-sum outcome likely
- Opponent uses positional tactics

**Integrative** — apply when:
- Multiple issues allow trade-offs (Bargaining Mix)
- Long-term relationship is important
- Both parties have compatible underlying interests
- Creative packaging can expand total value

**Mixed** — apply when features of both types are present.

---

## Transformation Rules

1. **Clarify ambiguity**: If the user says "fair deal", translate to a
   quantitative or observable target (e.g., "rate within 10% of market
   benchmark")
2. **Build Bargaining Mix**: Identify all issues at stake — not just the
   headline issue — and assess their priority and interdependence
3. **Separate interests from positions**: Infer the *why* behind stated
   goals where possible
4. **Classify negotiation type**: State whether the scenario is
   distributive, integrative, or mixed, and explain briefly why
5. **Estimate opponent profile**: Based on context clues, assign a type
   and estimate their likely BATNA and resistance point
6. **Validate BATNA**: Ensure the stated BATNA is realistic and distinct
   from the resistance point

---

## Example Transformation

**Input:**
```
Topic:         Freelance contract terms
Your Goal:     $60/hour with remote flexibility
Your Baseline: $50/hour, full remote
BATNA:         Stay in current role at $45/hour
Counterparty:  Growing startup, budget-conscious, needs senior dev
Context:       First engagement, no prior relationship
```

**Output:**
```json
{
  "scenario": {
    "topic": "Freelance contract rate and working conditions",
    "negotiation_type": "mixed",
    "negotiation_type_rationale": "Rate is distributive (fixed budget
      vs. rate demand), but flexibility, hours, and contract length
      allow integrative packaging.",

    "your_position": {
      "target_point": "$60/hour, 100% remote, flexible hours",
      "resistance_point": "$50/hour, full remote guaranteed",
      "batna": "Continue current role at $45/hour",
      "non_negotiables": ["100% remote work"],
      "flexibility_areas": ["rate", "contract length", "payment schedule"]
    },

    "bargaining_mix": [
      { "issue": "Hourly rate",       "priority": "high",   "linked_to": "contract length", "type": "tangible" },
      { "issue": "Remote work",       "priority": "high",   "linked_to": null,              "type": "tangible" },
      { "issue": "Contract length",   "priority": "medium", "linked_to": "hourly rate",     "type": "tangible" },
      { "issue": "Payment schedule",  "priority": "low",    "linked_to": null,              "type": "tangible" },
      { "issue": "Project ownership", "priority": "medium", "linked_to": null,              "type": "intangible" }
    ],

    "interests": {
      "substantive":  ["income above $50/hour", "location flexibility"],
      "process":      ["quick decision — opportunity cost of waiting"],
      "relational":   ["potential for long-term engagement"]
    },

    "opponent_profile": {
      "type": "analytical",
      "likely_batna": "Hire junior developer at lower rate",
      "likely_interests": ["cost control", "reliable delivery", "speed"],
      "likely_resistance_point": "$55/hour",
      "likely_strategy": "distributive on rate, integrative on structure"
    },

    "success_metrics": [
      "Hourly rate >= $50/hour",
      "100% remote clause included in contract",
      "Contract signed within 2 meetings"
    ]
  }
}
```
