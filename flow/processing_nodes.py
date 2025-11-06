"""Define LangGraph nodes for the chatbot and inject a system prompt from YAML (with fallback)."""

from typing import List  # Message list typing for readability

# LangChain message primitives used by chat models
from langchain_core.messages import (
    HumanMessage,   # represents user input
    AIMessage,      # represents model output
    BaseMessage,    # base protocol for chat messages
    SystemMessage,  # represents system instructions (behavior scaffold)
)

from flow.state import ChatbotState  # Shared typed state for the graph (TypedDict)
from services.gemini_client import gemini_client  # Preconfigured Gemini LLM client (singleton)
from services.standard_logger import logger  # Application logger (console + rotating file)

# YAML prompt loader (validated by Pydantic); raises on missing/invalid file
# If the YAML file is not available, we will apply a safe, local fallback below.
from utils.prompt_loader import load_prompt


def process_user_input(state: ChatbotState) -> ChatbotState:
    """
    Convert raw user text into chat messages and attach them to the graph state.

    Behavior:
      - Loads a system prompt (persona & rules) from `prompts/assistant.yaml`.
      - If the file is not found or is invalid, uses a safe default persona.
      - Appends both the SystemMessage and the HumanMessage to `messages`.

    Notes:
      - This node intentionally injects the system message on each turn because the
        caller provides a fresh empty `messages` list per user iteration.
      - If you ever preserve history across turns, consider guarding to avoid
        duplicating the system message (e.g., check for existing SystemMessage first).
    """
    current_input = state.get("current_input", "")
    if not current_input:
        # Defensive: graph entry without text—skip downstream execution
        logger.warning("Node: current_input vacío o no provisto.")
        return {}

    # --- Load system instructions from YAML (fallback if unavailable) ---
    try:
        prompt_cfg = load_prompt()  # reads prompts/assistant.yaml and validates fields
        system_text = prompt_cfg.persona  # single string with the assistant persona/instructions
    except Exception as e:
        # Safe fallback: concise, multilingual, spoiler-aware literary advisor
        logger.warning(f"Prompt YAML not available or invalid; using fallback. Detail: {e}")
        system_text = (
            "You are a well-read literary advisor. Detect the user's language (Spanish or English) "
            "and respond in the same language. Provide book recommendations, short summaries, "
            "and related titles in a formal yet enthusiastic tone. Keep answers concise but "
            "well-explained. Use bullet lists (book + brief context). Warn about spoilers."
        )

    logger.info(f"Node: Processing user input: {current_input[:120]}...")

    # Build the message delta for this step: system instructions + user input
    # LangGraph will merge this delta with the running state thanks to `add_messages`.
    new_messages = [
        SystemMessage(content=system_text),
        HumanMessage(content=current_input),
    ]
    return {"messages": new_messages}


def llm_response_node(state: ChatbotState) -> ChatbotState:
    """
    Call the Gemini chat model with the accumulated messages and attach the AI reply.

    Behavior:
      - Uses the `gemini_client` (LangChain ChatGoogleGenerativeAI) to invoke the model.
      - Stores both the AIMessage (for history) and plain text (for easy printing in the UI).
      - On error, logs the exception and returns a friendly message (keeps the loop alive).
    """
    # Ensure a list; when the graph starts a turn, upstream node provides a fresh message delta
    messages: List[BaseMessage] = state.get("messages", []) or []
    logger.info(f"Node: Generating LLM response using {len(messages)} message(s).")

    try:
        # Invoke the model using LangChain's chat message format
        ai_msg: AIMessage = gemini_client.get_llm_instance().invoke(messages)  # type: ignore
        text = ai_msg.content if hasattr(ai_msg, "content") else str(ai_msg)

        logger.info("LLM response received successfully.")
        # Attach the AI message (for conversation state) and a text field (for printing)
        return {"messages": [AIMessage(content=text)], "llm_response": text}

    except Exception as e:
        # Keep UX resilient: log the root cause and provide a safe reply
        logger.exception(f"Error invoking LLM: {e}")
        err = "Lo siento, ocurrió un error al procesar tu solicitud."
        return {"messages": [AIMessage(content=err)], "llm_response": err}