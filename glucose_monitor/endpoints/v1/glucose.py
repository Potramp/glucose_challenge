"""Glucose endpoint."""

from uuid import UUID
from loguru import logger
from datetime import datetime
from fastapi import status, APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from glucose_monitor.api_key import get_api_key
from glucose_monitor.queries.glucose_queries import get_glucose_reading_by_id
from glucose_monitor.queries.glucose_queries import get_glucose_for_user
from glucose_monitor.models.v1.model_glucose import GlucoseResponse


glucose_router = APIRouter()


@glucose_router.get(
    "/levels/",
    tags=["levels/"],
    summary=(
        "Retrieve ( GET ) a list of glucose levels for a given"
        "user_uuid , filter by start and stop timestamps (optional). This endpoint"
        "should support pagination, sorting, and a way to limit the number of"
        "glucose levels returned."
    ),
    response_description=("Paginated glucose levels data."),
    status_code=status.HTTP_200_OK,
)
def get_glucose_levels(
    user_uuid: UUID,
    start: datetime = None,
    stop: datetime = None,
    api_key=Depends(get_api_key),
    # page: int = 0,
    # entries_per_page: Annotated[int, Query(ge=1, le=100)] = settings.PAGE_SIZE,
) -> JSONResponse:
    """
    ## User Glucose level endpoint
    List glucose levels for a given user_uuid. Optional
    filters of start and stop timestamps. Supports
    pagination and sorting.
    Returns:
        Returns a JSON response with the Glucose levels data
    """
    logger.info("Looking for available glucose data.")
    glucose_levels = get_glucose_for_user(
        user_uuid,
        start,
        stop,
        # page,
        # entries_per_page,
    )
    encoded_glucose_levels = jsonable_encoder(glucose_levels)
    return JSONResponse(
        content=encoded_glucose_levels,
        # headers={
        #     "page": str(page or 1),
        #     "last-page": str((total_count + entries_per_page - 1) // entries_per_page),
        #     "total-count": str(total_count),
        #     "page-size": str(entries_per_page),
        # },
    )


@glucose_router.get(
    "/level/",
    tags=["level/"],
    summary=(
        "Retrieve a glucose reading from "
        "entry_id , filter by start and stop timestamps (optional). This endpoint"
        "should support pagination, sorting, and a way to limit the number of"
        "glucose levels returned."
    ),
    response_description=("Paginated glucose levels data."),
    status_code=status.HTTP_200_OK,
)
def get_glucose_levels_by_id(
    entry_id: UUID,
    api_key=Depends(get_api_key),
) -> list[GlucoseResponse]:
    """
    ## Single reading Glucose level endpoint
    Retrieve a glucose reading from entry_id.
    Returns:
        Returns a JSON response with the Glucose levels data
    """
    logger.info("Looking for available glucose data.")
    glucose_levels = get_glucose_reading_by_id(
        entry_id,
    )
    return glucose_levels
