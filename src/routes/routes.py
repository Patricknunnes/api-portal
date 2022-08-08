from fastapi import FastAPI

from src.routes.role_routes import role_router


def include_routes(app: FastAPI):
    app.include_router(role_router)
