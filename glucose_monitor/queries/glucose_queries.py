"""Queries to glucose DB."""

from uuid import UUID
from datetime import datetime
from typing import Any
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from sqlalchemy.sql.selectable import Select
from glucose_monitor.database import DB_ENGINE, GlucoseLevel
from glucose_monitor.models.v1.model_glucose import GlucoseResponse
from glucose_monitor.custom_exceptions import NoDataFoundError
from glucose_monitor.utils import parse_glucose_level
from glucose_monitor.utils import parse_glucose_levels, get_offset


def get_select_statement(
    user_id: UUID,
    page: int,
    entries_per_page: int,
    start: datetime | None = None,
    stop: datetime | None = None,
    is_count: bool = False,
) -> Select[Any]:
    """Get the count or select statement."""
    if is_count:
        statement = select(func.count(GlucoseLevel.uuid).label("total_results")).where(
            GlucoseLevel.user_uuid == user_id
        )
        if start and stop:
            statement = statement.where(GlucoseLevel.device_timestamp >= start).where(
                GlucoseLevel.device_timestamp <= stop
            )
    else:
        offset = get_offset(page, entries_per_page)
        statement = select(GlucoseLevel).where(GlucoseLevel.user_uuid == user_id)
        if start and stop:
            statement = statement.where(GlucoseLevel.device_timestamp >= start).where(
                GlucoseLevel.device_timestamp <= stop
            )
        statement = statement.offset(offset).limit(entries_per_page)

    return statement


def get_glucose_for_user(
    user_uuid: UUID,
    start: datetime | None,
    stop: datetime | None,
    page: int,
    entries_per_page: int,
) -> tuple[list[GlucoseResponse], int]:
    """Select glucose levels for user."""
    count_statement = get_select_statement(
        user_id=user_uuid,
        page=page,
        entries_per_page=entries_per_page,
        is_count=True,
    )
    select_statement = get_select_statement(
        user_id=user_uuid,
        page=page,
        entries_per_page=entries_per_page,
        is_count=False,
    )
    with Session(DB_ENGINE) as session:
        count_result = session.execute(count_statement)
        select_result = session.execute(select_statement)
        total_count = count_result.first()[0]  # type: ignore
        rows = select_result.all()
        if total_count == 0 or len(rows) == 0:
            raise NoDataFoundError()
        parsed_glucose_levels = parse_glucose_levels(rows)
    return parsed_glucose_levels, total_count


def get_glucose_reading_by_id(
    entry_id: UUID,
):
    """Select single glucose reading."""
    with Session(DB_ENGINE) as session:
        statement = select(
            GlucoseLevel,
        ).where(GlucoseLevel.uuid == entry_id)
        rows = session.execute(statement).first()
        if len(rows) == 0:
            raise NoDataFoundError()
        parsed_glucose_level = parse_glucose_level(rows)
    return parsed_glucose_level
