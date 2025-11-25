"""
Build and compile the LangGraph state graph that orchestrates the chatbot flow.
"""

from langgraph.graph import StateGraph, END
from app.services.state import ChatbotState
from app.services.processing_nodes import process_user_input, llm_response_node
from app.services.standard_logger import logger as default_logger


def build_graph(custom_logger=None):
    """
    Build and compile the main LangGraph StateGraph for the chatbot.

    Args:
        custom_logger: Optional custom logger instance. Defaults to standard logger.

    Returns:
        Compiled LangGraph application ready for execution.
    """
    log = custom_logger or default_logger
    try:
        log.info("Building the LangGraph structure.")

        # Create a graph that operates on the ChatbotState dictionary
        graph_builder: StateGraph[ChatbotState] = StateGraph(ChatbotState)  # type: ignore[type-arg]

        # Register the nodes of the pipeline
        graph_builder.add_node("user_input_processor", process_user_input)
        graph_builder.add_node("llm_executor", llm_response_node)

        # Set the entry point of the graph
        graph_builder.set_entry_point("user_input_processor")

        # Define the flow: user input -> LLM -> END
        graph_builder.add_edge("user_input_processor", "llm_executor")
        graph_builder.add_edge("llm_executor", END)

        # Compile the graph into an executable app
        app_graph = graph_builder.compile()
        log.info("LangGraph successfully compiled.")
        return app_graph

    except Exception as e:
        log.error(f"Error while building LangGraph: {e}")
        raise
