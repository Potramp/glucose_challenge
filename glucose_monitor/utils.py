"""Utility functions."""

from loguru import logger
from glucose_monitor.custom_exceptions import ParsingError
from glucose_monitor.models.v1.model_glucose import GlucoseResponse


def parse_glucose_level(rows: list) -> GlucoseResponse:
    """Parse db data into object."""
    try:
        parsed_rows = []
        for row in rows:
            glucose_level = GlucoseResponse(
                uuid=row.uuid,
                user_uuid=row.user_uuid,
                device=row.device,
                device_id=row.device_id,
                device_timestamp=row.device_timestamp,
                recording_type=row.recording_type,
                glucose_value_history=row.glucose_value_history,
                glucose_scan=row.glucose_scan,
            )
            parsed_rows.append(glucose_level)
        return parsed_rows
    except Exception as exc:
        message = (
            "Cannot parse data from DB! "
            "Check the ORM and parsing function.\n"
            f"Exception: {str(exc)}"
        )
        logger.error(message)
        raise ParsingError(message) from None
