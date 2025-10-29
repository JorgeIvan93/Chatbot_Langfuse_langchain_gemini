"""Define the node functions used by the LangGraph chatbot."""

from typing import List  # message list typing
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage  # LangChain message types
from flow.state import ChatbotState  # shared typed state for the graph
from services.gemini_client import gemini_client  # preconfigured Gemini LLM client
from services.standard_logger import logger  # app logger


def process_user_input(state: ChatbotState) -> ChatbotState:
    """Turn the raw user input into a HumanMessage and attach it to the state."""
    current_input = state.get("current_input", "")
    if not current_input:
        # Defensive: graph entry without text—skip downstream execution
        logger.warning("Node: current_input vacío o no provisto.")
        return {}

    logger.info(f"Node: Processing user input: {current_input[:120]}...")
    # Add the user's message; LangGraph will merge messages across nodes
    return {"messages": [HumanMessage(content=current_input)]}


def llm_response_node(state: ChatbotState) -> ChatbotState:
    """Call the Gemini chat model with the messages and attach the AI reply."""
    messages: List[BaseMessage] = state.get("messages", []) or []  # ensure a list
    logger.info(f"Node: Generating LLM response using {len(messages)} message(s).")

    try:
        # Invoke the model using the same message format used by LangChain chat models
        ai_msg: AIMessage = gemini_client.get_llm_instance().invoke(messages)  # type: ignore
        text = ai_msg.content if hasattr(ai_msg, "content") else str(ai_msg)

        logger.info("LLM response received successfully.")
        # Attach both the message (for history) and a text field (for easy printing)
        return {"messages": [AIMessage(content=text)], "llm_response": text}

    except Exception as e:
        # On error, keep a friendly message in the state to avoid breaking the loop
        logger.exception(f"Error invoking LLM: {e}")
        err = "Lo siento, ocurrió un error al procesar tu solicitud."
        return {"messages": [AIMessage(content=err)], "llm_response": err}