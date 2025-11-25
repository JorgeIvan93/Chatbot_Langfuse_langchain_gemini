from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from app.core.config import settings
from app.services.gemini_client import gemini_client
from app.utils.langfuse_traces import langfuse_client

router = APIRouter(tags=["Chatbot"])
security = HTTPBearer()  

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Verify JWT token from Authorization header.
    """
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/", summary="Chat endpoint (requires Bearer token)")
async def chatbot(
    message: str = Query(..., description="User message for the chatbot"),
    username: str = Depends(verify_token)
):
    """
    Chatbot endpoint:
    - Requires Bearer token.
    - Records Langfuse spans/generations.
    - Invokes Gemini model and returns response.
    """
    try:
        response_text = None

        if langfuse_client:
            with langfuse_client.start_as_current_observation(as_type="span", name="chatbot_request") as span:
                span.update(input=message, metadata={"user_id": username})

                with langfuse_client.start_as_current_observation(
                    as_type="generation",
                    name="gemini.invoke",
                    model=settings.gemini_model,
                    metadata={"temperature": settings.llm_temperature},
                ) as gen:
                    response_text = gemini_client.invoke_model(message)
                    gen.update(input=message, output=response_text)

                span.update(output=response_text)
                langfuse_client.update_current_trace(metadata={"endpoint": "/api/v1/chatbot"})
        else:
            response_text = gemini_client.invoke_model(message)

        return {"user": username, "message": message, "response": response_text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")
