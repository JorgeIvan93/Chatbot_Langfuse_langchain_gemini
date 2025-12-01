from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.routes import api_router
from app.services.standard_logger import logger
from fastapi.openapi.utils import get_openapi
from app.db.init_db import init_db

app = FastAPI(
    title="LangGraph Gemini Chatbot API",
    description="API for chatbot powered by LangGraph and Gemini LLM.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    """
    - Create SQLite tables automatically from ORM models.
    """
    init_db()


@app.get("/")
def root():
    return {"message": "Chatbot API is running. Use chatbot endpoint."}


app.include_router(api_router)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error. Please try again later."},
    )


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    # Ensure /auth/token is not protected by security
    for path, path_item in openapi_schema.get("paths", {}).items():
        if path == "/auth/token":
            for method_name, method_obj in path_item.items():
                if isinstance(method_obj, dict):
                    method_obj.pop("security", None)

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
