"""
Main application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from app.api.routes import health
from app.api.routes import docker_sdk
from app.api.openapi_config import get_openapi_tags, swagger_ui_parameters
from config.settings import settings

# Custom OpenAPI schema
def custom_openapi():
    """Custom OpenAPI schema configuration"""
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=settings.api_title,
        version=settings.api_version,
        description="API RESTful para SaaS Docker SDK PoC com Swagger/OpenAPI integrado",
        routes=app.routes,
        tags=get_openapi_tags(),
    )
    
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app = FastAPI(
    title=settings.api_title,
    description="API RESTful para SaaS Docker SDK PoC com Swagger/OpenAPI integrado",
    version=settings.api_version,
    docs_url=settings.docs_url,           # Swagger UI
    redoc_url=settings.redoc_url,         # ReDoc
    openapi_url=settings.openapi_url,     # OpenAPI schema
    swagger_ui_parameters=swagger_ui_parameters if settings.enable_swagger else {},
)

# Custom OpenAPI
if settings.enable_swagger:
    app.openapi = custom_openapi

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(docker_sdk.router, prefix="/api", tags=["docker-sdk"])


@app.get("/", tags=["root"])
async def root():
    """
    Root endpoint da API
    
    Retorna uma mensagem de confirmação que a API está rodando
    """
    return {
        "message": "API is running",
        "docs": "/docs",
        "redoc": "/redoc",
        "openapi": "/openapi.json"
    }
