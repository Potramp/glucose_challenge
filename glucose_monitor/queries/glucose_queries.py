"""Queries to glucose DB."""

from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session
from glucose_monitor.database import DB_ENGINE, GlucoseLevel
from glucose_monitor.custom_exceptions import NoDataFoundError
from glucose_monitor.utils import parse_glucose_level


def get_glucose_for_user(user_id: UUID):
    """Select glucose levels for user."""
    with Session(DB_ENGINE) as session:
        statement = (
            select(GlucoseLevel).where(GlucoseLevel.user_uuid == user_id)
            # .where(GlucoseLevel.user_uuid == user_id)
            # .where(GlucoseLevel.user_uuid == user_id)
        )
        rows = session.execute(statement).all()
        if len(rows) == 0:
            raise NoDataFoundError()
    return rows


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
