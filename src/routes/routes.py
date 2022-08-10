from fastapi import FastAPI

from src.routes.role_routes import role_router
from src.routes.user_routes import user_router


def include_routes(app: FastAPI):
    app.include_router(role_router)
    app.include_router(user_router)
