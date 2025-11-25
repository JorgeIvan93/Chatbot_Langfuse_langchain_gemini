from app.services.graph_builder import build_graph
from app.services.state import ChatbotState


async def run_chat_flow(message: str) -> str:
    """
    Executes the LangGraph flow with the given user message and returns the LLM response.
    """
    # Build the LangGraph flow
    graph = build_graph()

    # Define the initial state
    initial_state: ChatbotState = {
        "current_input": message,
        "messages": [],
    }

    # Execute the graph asynchronously
    result = await graph.ainvoke(initial_state)

    # Extract and return the final response
    return result.get("llm_response", "")
