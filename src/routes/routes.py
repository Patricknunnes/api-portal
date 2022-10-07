from fastapi import FastAPI

from src.routes.role_routes import role_router
from src.routes.user_routes import user_router
from src.routes.auth_routes import auth_router
from src.routes.utils_routes import util_router


def include_routes(app: FastAPI):
    app.include_router(role_router)
    app.include_router(user_router)
    app.include_router(auth_router)
    app.include_router(util_router)
