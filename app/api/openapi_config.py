"""
OpenAPI/Swagger configuration
"""
from typing import Dict, Any


def get_openapi_tags() -> list[Dict[str, Any]]:
    """Define OpenAPI tags with descriptions"""
    return [
        {
            "name": "root",
            "description": "Endpoints raiz da API",
        },
        {
            "name": "health",
            "description": "Verificação de saúde da API",
        },
    ]


def get_openapi_servers() -> list[Dict[str, str]]:
    """Define OpenAPI servers"""
    return [
        {
            "url": "http://localhost:8000",
            "description": "Servidor de Desenvolvimento",
        },
        {
            "url": "https://api.example.com",
            "description": "Servidor de Produção",
        },
    ]


swagger_ui_parameters = {
    "deepLinking": True,
    "displayOperationId": False,
    "defaultModelsExpandDepth": 1,
    "defaultModelExpandDepth": 1,
    "showExtensions": False,
    "showCommonExtensions": False,
    "layout": "BaseLayout",
}
