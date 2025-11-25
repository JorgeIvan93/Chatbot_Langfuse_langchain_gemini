"""
Defines LangGraph nodes for the chatbot and injects a system prompt from YAML (with fallback).
"""

from typing import List
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage, SystemMessage
from app.services.state import ChatbotState
from app.services.gemini_client import gemini_client
from app.services.standard_logger import logger
from app.utils.prompt_loader import load_prompt


def process_user_input(state: ChatbotState) -> ChatbotState:
    """
    Convert raw user input into chat messages and attach them to the graph state.

    Steps:
    - Load system prompt from `prompts/assistant.yaml`.
    - If YAML is missing or invalid, use a fallback prompt.
    - Add SystemMessage and HumanMessage to the message list.
    """
    current_input = state.get("current_input", "")
    if not current_input:
        logger.warning("Node: current_input is empty or missing.")
        return {}

    try:
        prompt_cfg = load_prompt()
        system_text = prompt_cfg.persona
    except Exception as e:
        logger.warning(
            f"Prompt YAML not available or invalid; using fallback. Detail: {e}"
        )
        system_text = (
            "You are a well-read literary advisor. Detect the user's language (Spanish or English) "
            "and respond in the same language. Provide book recommendations, short summaries, "
            "and related titles in a formal yet enthusiastic tone. Keep answers concise but "
            "well-explained. Use bullet lists (book + brief context). Warn about spoilers."
        )

    logger.info(f"Node: Processing user input: {current_input[:120]}...")

    new_messages = [
        SystemMessage(content=system_text),
        HumanMessage(content=current_input),
    ]
    return {"messages": new_messages}


def llm_response_node(state: ChatbotState) -> ChatbotState:
    """
    Call the Gemini chat model with accumulated messages and attach the AI reply.

    Steps:
    - Use `gemini_client` to invoke the model.
    - Store AIMessage and plain text response in the state.
    - On error, log the exception and return a fallback message.
    """
    messages: List[BaseMessage] = state.get("messages", []) or []
    logger.info(f"Node: Generating LLM response using {len(messages)} message(s).")

    try:
        ai_msg: AIMessage = gemini_client.get_llm_instance().invoke(messages)  # type: ignore
        text = ai_msg.content if hasattr(ai_msg, "content") else str(ai_msg)

        logger.info("LLM response received successfully.")
        return {"messages": [AIMessage(content=text)], "llm_response": text}

    except Exception as e:
        logger.exception(f"Error invoking LLM: {e}")
        err = "Sorry, an error occurred while processing your request."
        return {"messages": [AIMessage(content=err)], "llm_response": err}
