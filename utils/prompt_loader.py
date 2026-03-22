"""Utility for loading and parsing markdown-based agent and prompt definitions."""

import os
from pathlib import Path
from typing import Dict, Any, Optional
import yaml


def load_markdown_file(filepath: str) -> tuple[Dict[str, Any], str]:
    """
    Load a markdown file with YAML frontmatter.

    Returns: (frontmatter_dict, content_string)
    Raises: FileNotFoundError if file doesn't exist
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            try:
                frontmatter = yaml.safe_load(parts[1]) or {}
                body = parts[2].strip()
                return frontmatter, body
            except yaml.YAMLError:
                return {}, content

    return {}, content


def load_agent(agent_name: str, agents_dir: str = "agents") -> Dict[str, Any]:
    """
    Load an agent definition by name.

    Args:
        agent_name: "cooperative", "hardball", "skeptical", "analytical",
                    or "reflection"
        agents_dir: path to agents directory

    Returns: Dict with meta (role, tone, objectives, constraints,
             theory_basis) and content
    """
    filepath = os.path.join(agents_dir, f"opponent_{agent_name}.md")
    if agent_name == "reflection":
        filepath = os.path.join(agents_dir, "reflection_agent.md")

    frontmatter, body = load_markdown_file(filepath)
    return {
        "name": agent_name,
        "meta": frontmatter,
        "content": body,
        "filepath": filepath
    }


def load_prompt(prompt_name: str, prompts_dir: str = "prompts") -> Dict[str, Any]:
    """
    Load a prompt template by name.

    Args:
        prompt_name: "scenario_builder" or "feedback_template"
        prompts_dir: path to prompts directory

    Returns: Dict with meta (name, description) and content
    """
    filepath = os.path.join(prompts_dir, f"{prompt_name}.md")
    frontmatter, body = load_markdown_file(filepath)
    return {
        "name": prompt_name,
        "meta": frontmatter,
        "content": body,
        "filepath": filepath
    }


def available_agents(agents_dir: str = "agents") -> list[str]:
    """List available opponent agent names."""
    agents = []
    opponent_agents = ["cooperative", "hardball", "skeptical", "analytical"]
    for name in opponent_agents:
        filepath = os.path.join(agents_dir, f"opponent_{name}.md")
        if os.path.exists(filepath):
            agents.append(name)
    return agents


def get_agent_behavior(agent: Dict[str, Any]) -> str:
    """
    Extract the full behavior specification from an agent definition.

    Includes both the Theoretical Basis and Behavior Guidelines sections
    so the LLM receives the complete theoretical grounding alongside the
    concrete behavioral instructions.

    Args:
        agent: agent dict as returned by load_agent()

    Returns:
        String containing Theoretical Basis + Behavior Guidelines,
        or full content if section markers are absent.
    """
    content = agent.get("content", "")
    sections: list[str] = []

    # --- Theoretical Basis (new section in theory-grounded agents) ---
    if "## Theoretical Basis" in content:
        theory_section = content.split("## Theoretical Basis")[1]
        # Stop at the next ## heading
        next_heading = _next_section(theory_section)
        if next_heading:
            theory_section = theory_section[:next_heading]
        sections.append("## Theoretical Basis\n" + theory_section.strip())

    # --- Behavior Guidelines ---
    if "## Behavior Guidelines" in content:
        behavior_section = content.split("## Behavior Guidelines")[1]
        # Stop before Example block to keep the prompt focused
        if "## Example" in behavior_section:
            behavior_section = behavior_section.split("## Example")[0]
        sections.append("## Behavior Guidelines\n" + behavior_section.strip())

    if sections:
        return "\n\n".join(sections)

    # Fallback: return full content minus the Example block
    if "## Example" in content:
        return content.split("## Example")[0].strip()
    return content


def get_theory_basis(agent: Dict[str, Any]) -> str:
    """
    Return the theory_basis string from YAML frontmatter, if present.

    Useful for building concise system-prompt headers that cite the
    theoretical source without including the full Theoretical Basis prose.

    Args:
        agent: agent dict as returned by load_agent()

    Returns:
        theory_basis string, or empty string if not set.
    """
    return agent.get("meta", {}).get("theory_basis", "")


def get_feedback_structure(prompts_dir: str = "prompts") -> str:
    """Get feedback template structure for the reflection agent."""
    prompt = load_prompt("feedback_template", prompts_dir)
    content = prompt.get("content", "")
    if "## Output Structure" in content:
        output = content.split("## Output Structure")[1]
        if "## Feedback Principles" in output:
            output = output.split("## Feedback Principles")[0]
        return output.strip()
    return content


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _next_section(text: str) -> Optional[int]:
    """Return the character index of the next ## heading in text, or None."""
    lines = text.split("\n")
    char_index = 0
    for line in lines:
        if line.startswith("## "):
            return char_index if char_index > 0 else None
        char_index += len(line) + 1  # +1 for the newline
    return None
