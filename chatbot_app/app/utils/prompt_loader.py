# app/utils/prompt_loader.py
# Purpose: Load and validate the assistant prompt configuration from YAML using Pydantic.

from pathlib import Path
import yaml
from app.models.prompt_config import PromptConfig

# Absolute path based on current file location
DEFAULT_PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "assistant.yaml"


def load_prompt(path: str = str(DEFAULT_PROMPT_PATH)) -> PromptConfig:
    """
    Load and validate the prompt YAML file.
    """
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {path}")
    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return PromptConfig(**data)
