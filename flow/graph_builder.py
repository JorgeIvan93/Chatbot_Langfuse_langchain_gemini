"""Build and compile the LangGraph state graph that orchestrates the chatbot flow."""

from typing import Optional  # Type hinting for optional logger parameter
from langgraph.graph import StateGraph, END  # State machine builder and terminal marker
from flow.state import ChatbotState  # Typed state used by the graph
from flow.processing_nodes import process_user_input, llm_response_node  # Graph nodes
from services.standard_logger import logger as default_logger  # Application logger


# SRP: this module defines the graph structure (state, nodes, edges) and returns a compiled app graph.
def build_chat_graph(custom_logger=None):
    """Create and compile the main LangGraph StateGraph for the chatbot."""
    log = custom_logger or default_logger  # Allow overriding the logger when testing
    log.info("Building the LangGraph structure.")

    # Create a graph that works on our ChatbotState dictionary
    graph_builder: StateGraph[ChatbotState] = StateGraph(ChatbotState)  # type: ignore[type-arg]

    # Register the steps (nodes) of the pipeline
    graph_builder.add_node("user_input_processor", process_user_input)
    graph_builder.add_node("llm_executor", llm_response_node)

    # Select the first node to run when the graph starts
    graph_builder.set_entry_point("user_input_processor")

    # Connect nodes: user input -> LLM -> END
    graph_builder.add_edge("user_input_processor", "llm_executor")
    graph_builder.add_edge("llm_executor", END)

    # Compile to an executable app graph
    app_graph = graph_builder.compile()
    log.info("LangGraph successfully compiled.")
    return app_graph