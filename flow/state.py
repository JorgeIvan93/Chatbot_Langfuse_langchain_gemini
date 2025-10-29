"""
Typed state container used by LangGraph to carry inputs, messages, and outputs.
"""

from typing import TypedDict, Annotated, List, Optional  # TypedDict for explicit state shape; Annotated for add_messages
from langgraph.graph.message import add_messages  # helper to merge message lists across steps
from langchain_core.messages import BaseMessage  # base type for LangChain chat messages


class ChatbotState(TypedDict, total=False):
    # Last user input captured by the entry node
    current_input: str

    # Conversation history; `add_messages` merges lists when nodes return incremental messages
    messages: Annotated[List[BaseMessage], add_messages]

    # Final LLM-produced text for the turn (printed to console)
    llm_response: Optional[str]