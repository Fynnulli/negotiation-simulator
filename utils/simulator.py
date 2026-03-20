"""Core negotiation simulation engine."""

from typing import Any, Dict, Optional

from utils.llm_client import get_client
from utils.prompt_loader import get_agent_behavior, load_agent, load_prompt


def build_scenario(
    topic: str,
    goal: str,
    baseline: str,
    batna: str,
    counterparty: str,
    tone: str,
) -> Dict[str, Any]:
    """Build a structured negotiation scenario from user input."""
    # Ensure the scenario builder prompt exists and is loadable.
    _ = load_prompt("scenario_builder")

    user_input = f"""
Topic: {topic}
Your Goal: {goal}
Your Baseline: {baseline}
BATNA (walkaway): {batna}
Counterparty Description: {counterparty}
Context/Tone: {tone}
"""

    return {
        "topic": topic,
        "goal": goal,
        "baseline": baseline,
        "batna": batna,
        "counterparty": counterparty,
        "tone": tone,
        "raw_input": user_input.strip(),
    }


def run_negotiation(
    scenario: Dict[str, Any],
    opponent_type: str,
    your_opening: str,
    provider: Optional[str] = None,
) -> Dict[str, Any]:
    """Simulate a single-turn negotiation response from the selected opponent."""
    opponent_agent = load_agent(opponent_type)

    agent_role = opponent_agent.get("meta", {}).get("role", opponent_type)
    agent_tone = opponent_agent.get("meta", {}).get("tone", "")
    behavior = get_agent_behavior(opponent_agent)

    system_prompt = f"""
You are a {agent_role} in a negotiation.

Tone: {agent_tone}

Behavior Guidelines:
{behavior}

Scenario:
Topic: {scenario['topic']}
Counterparty: {scenario['counterparty']}
Context: {scenario['tone']}
"""

    negotiation_prompt = f"""
The user is proposing the following in a negotiation:

{your_opening}

Please respond as the {agent_role}. Your response should be natural, authentic, and reflect your negotiation style and objectives. Keep your response to 100-150 words.
"""

    client = get_client(provider=provider)
    opponent_response = client.generate(
        prompt=negotiation_prompt,
        system_prompt=system_prompt,
        max_tokens=500,
    )

    return {
        "opponent_type": opponent_type,
        "agent_role": agent_role,
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
    """Generate structured reflection feedback for the negotiation."""
    reflection_agent = load_agent("reflection")
    _ = load_prompt("feedback_template")

    agent_role = reflection_agent.get("meta", {}).get("role", "Reflection Agent")

    system_prompt = f"""
You are a {agent_role} analyzing a completed negotiation.

Your job is to provide structured, educational feedback on:
1. How well the user achieved their goal
2. Strategy effectiveness
3. Communication quality
4. Relationship building
5. Key moments and turning points
6. Development opportunities

Be balanced, specific, and constructive. Focus on learning.
"""

    reflection_prompt = f"""
Please analyze this negotiation:

GOAL: {scenario['goal']}
BASELINE: {scenario['baseline']}
BATNA: {scenario['batna']}

USER'S OPENING:
{negotiation_result['your_opening']}

OPPONENT RESPONSE:
{negotiation_result['opponent_response']}

Provide structured feedback covering:
1. Outcome vs. goal
2. Strategy used and effectiveness
3. Communication quality
4. Relationship dynamics
5. Key turning points
6. Development opportunity (highest impact)

Keep feedback under 400 words. Be specific and actionable.
"""

    client = get_client(provider=provider)
    reflection_output = client.generate(
        prompt=reflection_prompt,
        system_prompt=system_prompt,
        max_tokens=700,
    )

    return {"reflection": reflection_output, "structure": "See feedback sections above"}


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
    """Run the full pipeline: scenario -> negotiation -> reflection."""
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
