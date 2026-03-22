"""Core negotiation simulation engine."""

from typing import Any, Dict, Optional

from utils.llm_client import get_client
from utils.prompt_loader import (
    get_agent_behavior,
    get_theory_basis,
    load_agent,
    load_prompt,
)


def build_scenario(
    topic: str,
    goal: str,
    baseline: str,
    batna: str,
    counterparty: str,
    tone: str,
) -> Dict[str, Any]:
    """Build a structured negotiation scenario from user input.

    Maps to Lewicki et al. (2010) planning steps 1–7:
      - topic       → Step 1: Defining the Issues
      - goal        → Step 3: Defining Interests / Step 6: Targets
      - baseline    → Step 4: Defining Resistance Points
      - batna       → Step 5: Defining Alternatives (BATNA)
      - counterparty→ Step 8: Analyzing the Other Party
      - tone        → Step 7: Assessing Social Context
    """
    _ = load_prompt("scenario_builder")

    return {
        "topic": topic,
        "goal": goal,
        "baseline": baseline,
        "batna": batna,
        "counterparty": counterparty,
        "tone": tone,
        "raw_input": (
            f"Topic: {topic}\n"
            f"Your Goal: {goal}\n"
            f"Your Baseline (Resistance Point): {baseline}\n"
            f"BATNA (walkaway): {batna}\n"
            f"Counterparty: {counterparty}\n"
            f"Context / Tone: {tone}"
        ),
    }


def run_negotiation(
    scenario: Dict[str, Any],
    opponent_type: str,
    your_opening: str,
    provider: Optional[str] = None,
) -> Dict[str, Any]:
    """Simulate a single-turn negotiation response from the selected opponent.

    The system prompt includes:
      - The agent's theoretical basis (e.g. distributive bargaining,
        Harvard Concept) drawn from the theory_basis YAML field and the
        Theoretical Basis markdown section.
      - The agent's concrete Behavior Guidelines.

    This ensures the LLM embodies both the scientific model and the
    practical behavioral instructions.
    """
    opponent_agent = load_agent(opponent_type)
    meta = opponent_agent.get("meta", {})

    agent_role = meta.get("role", opponent_type)
    agent_tone = meta.get("tone", "")
    theory_basis = get_theory_basis(opponent_agent)
    behavior = get_agent_behavior(opponent_agent)

    # Build theory header line for system prompt
    theory_header = (
        f"Theoretical basis: {theory_basis}\n" if theory_basis else ""
    )

    system_prompt = f"""You are a {agent_role} in a negotiation simulation.

{theory_header}Tone: {agent_tone}

{behavior}

Scenario context:
Topic: {scenario['topic']}
Counterparty (that's you): {scenario['counterparty']}
Setting: {scenario['tone']}
"""

    negotiation_prompt = f"""The user is making the following opening in a negotiation:

\"\"\"{your_opening}\"\"\"

Respond as the {agent_role}. Your response must:
- Authentically reflect your negotiation style, theoretical approach, and objectives
- React to the specific content of their opening
- Be 100–150 words maximum

Do not break character or explain your strategy. Just negotiate."""

    client = get_client(provider=provider)
    opponent_response = client.generate(
        prompt=negotiation_prompt,
        system_prompt=system_prompt,
        max_tokens=500,
    )

    return {
        "opponent_type": opponent_type,
        "agent_role": agent_role,
        "theory_basis": theory_basis,
        "your_opening": your_opening,
        "opponent_response": opponent_response,
        "conversation": [
            {"role": "user", "content": your_opening},
            {"role": "opponent", "content": opponent_response},
        ],
    }


def run_reflection(
    scenario: Dict[str, Any],
    negotiation_result: Dict[str, Any],
    provider: Optional[str] = None,
) -> Dict[str, Any]:
    """Generate structured reflection feedback grounded in negotiation theory.

    Feedback is structured around:
      - The four Harvard Principles (Fisher & Ury, 1981)
      - BATNA awareness (Lewicki et al., 2010, S. 125 f.)
      - Strategy-opponent fit
    """
    reflection_agent = load_agent("reflection")
    _ = load_prompt("feedback_template")

    agent_role = reflection_agent.get("meta", {}).get("role", "Negotiation Analyst")
    opponent_theory = negotiation_result.get("theory_basis", "")

    system_prompt = f"""You are a {agent_role} evaluating a negotiation simulation.

Your feedback framework is grounded in:
- The four Harvard Principles (Fisher & Ury, 1981):
    1. Separate people from the problem
    2. Focus on interests, not positions
    3. Invent options for mutual gain
    4. Insist on objective criteria
- BATNA awareness (Lewicki et al., 2010, S. 125 f.)
- Strategy-opponent fit: the opponent used {opponent_theory or 'a standard negotiation approach'}

Be specific, balanced, and actionable. Reference theory where relevant.
"""

    reflection_prompt = f"""Analyze this negotiation:

GOAL: {scenario['goal']}
RESISTANCE POINT (baseline): {scenario['baseline']}
BATNA: {scenario['batna']}

USER'S OPENING:
{negotiation_result['your_opening']}

OPPONENT RESPONSE ({negotiation_result['agent_role']}):
{negotiation_result['opponent_response']}

Structure your feedback across these sections:
1. Outcome vs. Goal
2. Harvard Principle 1 — People vs. Problem
3. Harvard Principle 2 — Interests vs. Positions
4. Harvard Principle 3 — Options for Mutual Gain
5. Harvard Principle 4 — Objective Criteria
6. BATNA Awareness
7. Strategy-Opponent Fit
8. Key Turning Point
9. Development Priority (one concrete next step)

Keep total feedback under 500 words. Be specific — quote or paraphrase the user's actual words."""

    client = get_client(provider=provider)
    reflection_output = client.generate(
        prompt=reflection_prompt,
        system_prompt=system_prompt,
        max_tokens=900,
    )

    return {
        "reflection": reflection_output,
        "framework": "Harvard Concept (Fisher & Ury, 1981) + Lewicki et al. (2010)",
    }


def simulate_negotiation(
    topic: str,
    goal: str,
    baseline: str,
    batna: str,
    counterparty: str,
    tone: str,
    opponent_type: str,
    your_opening: str,
    provider: Optional[str] = None,
) -> Dict[str, Any]:
    """Run the full pipeline: scenario → negotiation → reflection."""
    scenario = build_scenario(topic, goal, baseline, batna, counterparty, tone)
    negotiation = run_negotiation(scenario, opponent_type, your_opening, provider=provider)
    reflection = run_reflection(scenario, negotiation, provider=provider)

    return {
        "scenario": scenario,
        "negotiation": negotiation,
        "reflection": reflection,
        "provider": provider or "default",
        "success": True,
    }
