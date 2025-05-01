"""API Key module."""

from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN
from glucose_monitor.settings import settings

api_key_header = APIKeyHeader(name=settings.api_key_name, auto_error=False)


async def get_api_key(
    api_key_header: str = Security(api_key_header),
) -> str:
    """."""
    if api_key_header in settings.api_keys:
        return api_key_header
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Could not validate api key.",
        )
