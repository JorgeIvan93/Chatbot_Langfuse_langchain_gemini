"""
Loads and validates prompt configuration from YAML using Pydantic.
Provides a safe fallback if the file is missing or invalid.
"""

import yaml
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional


class PromptConfig(BaseModel):
    name: str
    version: str
    persona: str
    language: List[str]
    audience: str
    style: dict
    policy: dict
    generation: dict
    few_shot: Optional[List[dict]] = Field(default=[])


def load_prompt(path: str = "prompts/assistant.yaml") -> PromptConfig:
    """Load and validate the prompt YAML file."""
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {path}")
    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return PromptConfig(**data)