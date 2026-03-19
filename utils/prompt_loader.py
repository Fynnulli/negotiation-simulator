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
    
    # Parse YAML frontmatter (between --- markers)
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
        agent_name: "cooperative", "hardball", "skeptical", "analytical", or "reflection"
        agents_dir: path to agents directory
    
    Returns: Dict with meta (role, tone, objectives, constraints) and content
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
    """Extract behavior guidelines from agent definition."""
    content = agent.get("content", "")
    # Simple extraction: content after "## Behavior Guidelines" section
    if "## Behavior Guidelines" in content:
        behavior_section = content.split("## Behavior Guidelines")[1]
        if "## Example" in behavior_section:
            behavior_section = behavior_section.split("## Example")[0]
        return behavior_section.strip()
    return content


def get_feedback_structure(prompts_dir: str = "prompts") -> str:
    """Get feedback template structure for reflection."""
    prompt = load_prompt("feedback_template", prompts_dir)
    # Extract the "Output Structure" section
    content = prompt.get("content", "")
    if "## Output Structure" in content:
        return content.split("## Output Structure")[1].split("## Feedback Principles")[0].strip()
    return content
