import logging
from collections.abc import Awaitable, Callable
from functools import partial

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette import status
from starlette.requests import Request

from src.domain.exceptions.base import AppError
from src.domain.exceptions.tariff import TariffNotFoundError, UploadTariffsWhenStorageNotEmptyError
from src.presentation.webapi.schemas.responses import ErrorResponse

logger = logging.getLogger(__name__)


def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        UploadTariffsWhenStorageNotEmptyError, error_handler(status.HTTP_409_CONFLICT)
    )
    app.add_exception_handler(TariffNotFoundError, error_handler(status.HTTP_404_NOT_FOUND))
    app.add_exception_handler(AppError, error_handler(status.HTTP_500_INTERNAL_SERVER_ERROR))
    app.add_exception_handler(Exception, unknown_exception_handler)


def error_handler(status_code: int) -> Callable[..., Awaitable[JSONResponse]]:
    return partial(app_error_handler, status_code=status_code)


async def app_error_handler(request: Request, err: AppError, status_code: int) -> JSONResponse:
    return await handle_error(
        request=request,
        err=err,
        err_message=err.message,
        status_code=status_code,
    )


async def unknown_exception_handler(request: Request, err: Exception) -> JSONResponse:
    logger.error("Handle error", exc_info=err, extra={"error": err})
    return JSONResponse(
        ErrorResponse(message="Unknown error occurred").model_dump(),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


async def handle_error(
    request: Request,
    err: Exception,
    err_message: str,
    status_code: int,
) -> JSONResponse:
    logger.error("Handle error", exc_info=err, extra={"error": err})
    return JSONResponse(
        ErrorResponse(message=err_message).model_dump(),
        status_code=status_code,
    )
