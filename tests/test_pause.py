import json
import re

import pytest

from pause import models


@pytest.fixture
def day_data():
    return {
        "activities": {
            "0": [
                {"id": 0, "value": 16, "label": "", "color": "#DCDCDC"},
                {"id": 1, "value": 8, "label": "sleep", "color": "#ff6300"},
                {"id": "?", "value": "", "label": ""},
            ]
        },
        "chartTypes": {"0": "pie"},
        "timeUnit": "day",
        "month": None,
        "year": None,
    }


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_create_and_read_day_data(client, day_data):
    post_response = client.post("/api/pause/activities", json=day_data)

    assert post_response.status_code == 201
    activities_id = post_response.get_json()
    assert re.fullmatch(r"[A-Za-z0-9]{16}", activities_id)

    get_response = client.get(f"/api/pause/activities/{activities_id}")

    assert get_response.status_code == 200
    assert get_response.get_json() == {
        "activities": day_data["activities"],
        "chart_types": day_data["chartTypes"],
        "time_unit": "day",
        "month": None,
        "year": None,
    }


def test_create_and_read_month_data(client, day_data):
    payload = {
        **day_data,
        "timeUnit": "month",
        "month": "January",
        "year": 2026,
    }

    activities_id = client.post(
        "/api/pause/activities",
        json=payload,
    ).get_json()
    response = client.get(f"/api/pause/activities/{activities_id}")

    assert response.status_code == 200
    assert response.get_json()["month"] == "January"
    assert response.get_json()["year"] == 2026


@pytest.mark.parametrize(
    ("payload", "message"),
    [
        (None, "Request must contain activities and time unit"),
        (
            {"activities": [], "chartTypes": {}, "timeUnit": "day"},
            "Activities must be a dictionary",
        ),
        (
            {"activities": {}, "chartTypes": [], "timeUnit": "day"},
            "Chart types must be a dictionary",
        ),
        (
            {"activities": {}, "chartTypes": {}, "timeUnit": []},
            "Time unit must be a string",
        ),
        (
            {"activities": {}, "chartTypes": {}, "timeUnit": "year"},
            "Time unit must be day, week, or month",
        ),
        (
            {"activities": {}, "chartTypes": {}, "timeUnit": "month"},
            "Month data must contain a month and year",
        ),
    ],
)
def test_create_validation(client, payload, message):
    response = client.post("/api/pause/activities", json=payload)

    assert response.status_code == 400
    assert response.get_data(as_text=True) == message


def test_read_not_found(client):
    response = client.get("/api/pause/activities/missing")

    assert response.status_code == 404
    assert response.get_data(as_text=True) == "Activities not found"


def test_reads_rows_created_by_original_api(client, day_data):
    with models.session_scope() as session:
        session.add(
            models.Activities(
                external_id="legacy",
                activities=json.dumps(day_data["activities"]),
                chart_types=json.dumps(day_data["chartTypes"]),
                time_unit="day",
            )
        )

    response = client.get("/api/pause/activities/legacy")

    assert response.status_code == 200
    assert response.get_json()["activities"] == day_data["activities"]
    assert response.get_json()["chart_types"] == day_data["chartTypes"]
