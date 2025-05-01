"""ASGI."""

from loguru import logger
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from glucose_monitor.endpoints.v1.glucose import glucose_router
from glucose_monitor.database import create_db_and_tables
from glucose_monitor.custom_exceptions import NoDataFoundError, ParsingError


def setup_logging():
    """
    setup json logging to stdout
    """
    logger.remove()
    logger.add(
        sink="/dev/stdout",
        level="INFO",
        format="{message}",
        serialize=True,
    )


V1_PREFIX = "/api/v1"
app = FastAPI()
app.include_router(glucose_router, prefix=V1_PREFIX)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.exception_handler(NoDataFoundError)
async def no_data_found_exception_handler(
    request: Request,
    exc: NoDataFoundError,
) -> JSONResponse:
    """Handle NoDataFoundError exceptions."""
    return JSONResponse(
        status_code=404,
        content={"detail": [{"msg": f"NoDataFoundError: {exc.__str__()}"}]},
    )


@app.exception_handler(ParsingError)
async def parsing_error_exception_handler(
    request: Request,
    exc: ParsingError,
) -> JSONResponse:
    """Handle ParsingError exceptions."""
    return JSONResponse(
        status_code=404,
        content={"detail": [{"msg": f"ParsingError: {exc.__str__()}"}]},
    )
