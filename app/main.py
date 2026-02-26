from fastapi import FastAPI

from app.routes.items import router as containers_router
from app.routes.users import router as health_router

app = FastAPI(
    title="SaaS Docker SDK API",
    description="API para gerenciamento de containers Docker",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {
        "message": "SaaS Docker SDK API",
        "version": "1.0.0",
        "docs": "/docs"
    }

app.include_router(containers_router)
app.include_router(health_router)
