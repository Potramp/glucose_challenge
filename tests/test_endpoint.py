"""Test the glucose endpoint."""

from uuid import UUID
from datetime import datetime, timedelta
from inline_snapshot import snapshot
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from freezegun import freeze_time
from glucose_monitor.settings import settings
from glucose_monitor.database import GlucoseLevel

FROZEN_TIME = "2022-01-01"

API_KEY = settings.api_keys[0]

device_id = UUID("28bcc70a-5e92-49a7-9bb2-a764d9f7374b")
entry_uuid1 = UUID("01cc74e4-29c7-4425-8431-6d1a955a742f")
entry_uuid2 = UUID("20c8a1d4-5f32-4e25-adbd-cf80218cbb5a")
entry_uuid3 = UUID("328730b2-09d4-487e-acdf-17bca46ecb39")
user_uuid = UUID("291cdc81-1704-4be7-a0bb-735d94f85f1e")


@freeze_time(FROZEN_TIME)
def test_glucose_endpoint_by_entry(
    setup_datebase: Session,
    client: TestClient,
) -> None:
    # Given
    glucose_entry = GlucoseLevel(
        uuid=entry_uuid1,
        user_uuid=user_uuid,
        device="MyDevice",
        device_id=device_id,
        device_timestamp=datetime.now(),
        recording_type=0,
        glucose_value_history=13,
        glucose_scan=15,
    )
    setup_datebase.add(glucose_entry)
    setup_datebase.commit()
    url = f"/api/v1/level?entry_id={entry_uuid1}"
    # When
    response = client.get(url, headers={"apikey": API_KEY})
    # Then
    assert response.status_code == 200
    assert response.json() == snapshot(
        [
            {
                "uuid": "01cc74e4-29c7-4425-8431-6d1a955a742f",
                "device": "MyDevice",
                "device_id": "28bcc70a-5e92-49a7-9bb2-a764d9f7374b",
                "device_timestamp": "2022-01-01T00:00:00",
                "recording_type": 0,
                "glucose_value_history": 13,
                "glucose_scan": 15,
            }
        ]
    )


@freeze_time(FROZEN_TIME)
def test_glucose_endpoint_by_user_no_start_stop(
    setup_datebase: Session,
    client: TestClient,
) -> None:
    # Given
    glucose_entry = GlucoseLevel(
        uuid=entry_uuid1,
        user_uuid=user_uuid,
        device="MyDevice",
        device_id=device_id,
        device_timestamp=datetime.now(),
        recording_type=0,
        glucose_value_history=13,
        glucose_scan=15,
    )
    glucose_entry2 = GlucoseLevel(
        uuid=entry_uuid2,
        user_uuid=user_uuid,
        device="MyDevice",
        device_id=device_id,
        device_timestamp=datetime.now() + timedelta(days=1),
        recording_type=0,
        glucose_value_history=14,
        glucose_scan=16,
    )
    glucose_entry3 = GlucoseLevel(
        uuid=entry_uuid3,
        user_uuid=user_uuid,
        device="MyDevice",
        device_id=device_id,
        device_timestamp=datetime.now() + timedelta(days=2),
        recording_type=0,
        glucose_value_history=14,
        glucose_scan=16,
    )
    setup_datebase.add(glucose_entry)
    setup_datebase.add(glucose_entry2)
    setup_datebase.add(glucose_entry3)
    setup_datebase.commit()
    url = "/api/v1/levels"
    params = {
        "user_uuid": user_uuid,
    }
    # When
    response = client.get(url, params=params, headers={"apikey": API_KEY})
    # Then
    assert response.status_code == 200
    assert response.json() == snapshot(
        [
            {
                "uuid": "01cc74e4-29c7-4425-8431-6d1a955a742f",
                "device": "MyDevice",
                "device_id": "28bcc70a-5e92-49a7-9bb2-a764d9f7374b",
                "device_timestamp": "2022-01-01T00:00:00",
                "recording_type": 0,
                "glucose_value_history": 13,
                "glucose_scan": 15,
            },
            {
                "uuid": "20c8a1d4-5f32-4e25-adbd-cf80218cbb5a",
                "device": "MyDevice",
                "device_id": "28bcc70a-5e92-49a7-9bb2-a764d9f7374b",
                "device_timestamp": "2022-01-02T00:00:00",
                "recording_type": 0,
                "glucose_value_history": 14,
                "glucose_scan": 16,
            },
            {
                "uuid": "328730b2-09d4-487e-acdf-17bca46ecb39",
                "device": "MyDevice",
                "device_id": "28bcc70a-5e92-49a7-9bb2-a764d9f7374b",
                "device_timestamp": "2022-01-03T00:00:00",
                "recording_type": 0,
                "glucose_value_history": 14,
                "glucose_scan": 16,
            },
        ]
    )


@freeze_time(FROZEN_TIME)
def test_glucose_endpoint_by_user_with_start_stop(
    setup_datebase: Session,
    client: TestClient,
) -> None:
    # Given
    glucose_entry = GlucoseLevel(
        uuid=entry_uuid1,
        user_uuid=user_uuid,
        device="MyDevice",
        device_id=device_id,
        device_timestamp=datetime.now(),
        recording_type=0,
        glucose_value_history=13,
        glucose_scan=15,
    )
    glucose_entry2 = GlucoseLevel(
        uuid=entry_uuid2,
        user_uuid=user_uuid,
        device="MyDevice",
        device_id=device_id,
        device_timestamp=datetime.now() - timedelta(days=1),
        recording_type=0,
        glucose_value_history=14,
        glucose_scan=16,
    )
    glucose_entry3 = GlucoseLevel(
        uuid=entry_uuid3,
        user_uuid=user_uuid,
        device="MyDevice",
        device_id=device_id,
        device_timestamp=datetime.now() - timedelta(days=2),
        recording_type=0,
        glucose_value_history=14,
        glucose_scan=16,
    )
    setup_datebase.add(glucose_entry)
    setup_datebase.add(glucose_entry2)
    setup_datebase.add(glucose_entry3)
    setup_datebase.commit()
    url = "/api/v1/levels"
    params = {
        "user_uuid": user_uuid,
        "start": datetime.now() - timedelta(days=2),
        "stop": datetime.now() - timedelta(days=1),
    }
    # When
    response = client.get(url, params=params, headers={"apikey": API_KEY})
    # Then
    assert response.status_code == 200
    assert response.json() == snapshot(
        [{'uuid':'01cc74e4-29c7-4425-8431-6d1a955a742f','device':'MyDevice','device_id':'28bcc70a-5e92-49a7-9bb2-a764d9f7374b','device_timestamp':'2022-01-01T00:00:00','recording_type':0 ,'glucose_value_history':13 ,'glucose_scan':15 }, {
                "uuid": "20c8a1d4-5f32-4e25-adbd-cf80218cbb5a",
                "device": "MyDevice",
                "device_id": "28bcc70a-5e92-49a7-9bb2-a764d9f7374b",
                "device_timestamp": "2021-12-31T00:00:00",
                "recording_type": 0,
                "glucose_value_history": 14,
                "glucose_scan": 16,
            },
            {
                "uuid": "328730b2-09d4-487e-acdf-17bca46ecb39",
                "device": "MyDevice",
                "device_id": "28bcc70a-5e92-49a7-9bb2-a764d9f7374b",
                "device_timestamp": "2021-12-30T00:00:00",
                "recording_type": 0,
                "glucose_value_history": 14,
                "glucose_scan": 16,
            },
        ]
    )
