from fastapi import FastAPI

from src.presentation.webapi.handlers.default import default_router
from src.presentation.webapi.handlers.docs import register_static_docs_routes
from src.presentation.webapi.handlers.exceptions import setup_exception_handlers
from src.presentation.webapi.handlers.tariff import router as tariffs_router


def setup_handlers(app: FastAPI) -> None:
    register_static_docs_routes(app)
    setup_exception_handlers(app)

    app.include_router(default_router)
    app.include_router(tariffs_router)
