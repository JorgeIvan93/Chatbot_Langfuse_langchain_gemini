# app/models/prompt_config.py
# Purpose: Define Pydantic models for validating the assistant prompt configuration.

from pydantic import BaseModel
from typing import List


class StyleConfig(BaseModel):
    tone: str
    detail: str
    format: str


class PolicyConfig(BaseModel):
    avoid_topics: List[str]
    missing_info: str
    spoilers: str


class GenerationConfig(BaseModel):
    temperature: float
    top_p: float
    top_k: int
    max_output_tokens: int
    response_mime_type: str


class FewShotExample(BaseModel):
    user: str
    assistant: str


class PromptConfig(BaseModel):
    name: str
    version: str
    persona: str
    language: List[str]
    audience: str
    style: StyleConfig
    policy: PolicyConfig
    generation: GenerationConfig
    few_shot: List[FewShotExample]
