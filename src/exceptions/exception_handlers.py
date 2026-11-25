import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from exceptions.not_found_error import NotFoundError

# TODO: Maybe move this file to an other location, or merge it in main?

logger = logging.getLogger(__name__)


def handle_not_found(request: Request, error: NotFoundError) -> JSONResponse:
    logger.warning("%s %s -> 404: %s", request.method, request.url.path, error)

    return JSONResponse(
        status_code=404,
        content={"detail": str(error)}
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(NotFoundError, handle_not_found)
