"""Configs for tests."""

import pytest
from glucose_monitor.database import DB_ENGINE
from glucose_monitor.database import GlucoseLevel
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from glucose_monitor.asgi import app


@pytest.fixture
def client() -> TestClient:
    """Return TestClient for app."""
    client = TestClient(app)
    return client


@pytest.fixture
def setup_datebase():
    # Create schema on localhost db

    # Create the table itself
    GlucoseLevel.metadata.create_all(DB_ENGINE)

    session = Session(DB_ENGINE)
    yield session

    # teardown
    GlucoseLevel.metadata.drop_all(DB_ENGINE)
