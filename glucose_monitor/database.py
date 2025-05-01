"""Glucose DB engine and db creation"""

from uuid import UUID
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Mapped, mapped_column
from glucose_monitor.settings import db_settings


DB_ENGINE = create_engine(db_settings.db_url, connect_args={"check_same_thread": False})
session = sessionmaker(autocommit=False, autoflush=False, bind=DB_ENGINE)
Base = declarative_base()


class GlucoseLevel(Base):
    """Glucose levels table."""

    __tablename__ = "glucose_levels"

    uuid: Mapped[UUID] = mapped_column(primary_key=True)
    user_uuid: Mapped[UUID]
    device: Mapped[str] = mapped_column(primary_key=True)
    device_id: Mapped[UUID] = mapped_column(primary_key=True)
    device_timestamp: Mapped[datetime]
    recording_type: Mapped[int]
    glucose_value_history: Mapped[int]
    glucose_scan: Mapped[int]

    def __repr__(self) -> str:
        return (
            "GlucoseLevel("
            f"uuid={self.uuid},"
            f"user_uuid={self.user_uuid},"
            f"device={self.device},"
            f"device_id={self.device_id},"
            f"device_timestamp={self.device_timestamp},"
            f"recording_type={self.recording_type},"
            f"glucose_value_history={self.glucose_value_history},"
            f"glucose_scan={self.glucose_scan}"
            ")"
        )


def create_db_and_tables():
    """Create DB."""
    GlucoseLevel.metadata.create_all(DB_ENGINE)


def populate_table():
    """."""
    pass
