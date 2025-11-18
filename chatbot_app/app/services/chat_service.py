from app.services.graph_builder import build_graph
from app.services.standard_logger import logger

async def process_chat(request):
    try:
        # Log the incoming user message
        logger.info(f"Processing user message: {request.message}")

        # Build the LangGraph state graph
        graph = build_graph()

        # Initial state for graph execution (must match node expectations)
        initial_state = {
            "current_input": request.message  # Key expected by process_user_input node
        }

        # Execute the graph with the initial state
        result = graph.invoke(initial_state)

        # Extract the LLM response from the result state
        response = result.get("llm_response", "No response generated")

        # Return both user input and chatbot response
        return {
            "user_message": request.message,
            "reply": response
        }

    except Exception as e:
        # Log any unexpected error and return a safe response
        logger.error(f"Error in process_chat: {e}")
        return {"error": "Failed to process chat"}