"""Queries to glucose DB."""

from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session
from glucose_monitor.database import DB_ENGINE, GlucoseLevel
from glucose_monitor.custom_exceptions import NoDataFoundError
from glucose_monitor.utils import parse_glucose_level
from glucose_monitor.utils import parse_glucose_levels
from datetime import datetime


def get_glucose_for_user(
    user_id: UUID,
    start: datetime | None,
    stop: datetime | None,
):
    """Select glucose levels for user."""
    with Session(DB_ENGINE) as session:
        statement = select(GlucoseLevel).where(GlucoseLevel.user_uuid == user_id)
        if start and stop:
            statement = statement.where(GlucoseLevel.device_timestamp >= start).where(
                GlucoseLevel.device_timestamp <= stop
            )
        rows = session.execute(statement).all()
        if len(rows) == 0:
            raise NoDataFoundError()
        parsed_glucose_levels = parse_glucose_levels(rows)
    return parsed_glucose_levels


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
