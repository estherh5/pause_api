import json
import secrets
import string

from flask import Blueprint, jsonify, make_response, request
from sqlalchemy import select

from pause import models

api = Blueprint("pause", __name__)
EXTERNAL_ID_ALPHABET = string.ascii_letters + string.digits
VALID_TIME_UNITS = {"day", "week", "month"}


def generate_external_id(length=16):
    return "".join(secrets.choice(EXTERNAL_ID_ALPHABET) for _ in range(length))


def decode_json_value(value):
    # Rows created by the original API stored JSON strings inside JSON columns.
    return json.loads(value) if isinstance(value, str) else value


def validate_payload(data):
    if (
        not data
        or "activities" not in data
        or "chartTypes" not in data
        or "timeUnit" not in data
    ):
        return "Request must contain activities and time unit"

    if not isinstance(data["activities"], dict):
        return "Activities must be a dictionary"

    if not isinstance(data["chartTypes"], dict):
        return "Chart types must be a dictionary"

    if not isinstance(data["timeUnit"], str):
        return "Time unit must be a string"

    if data["timeUnit"] not in VALID_TIME_UNITS:
        return "Time unit must be day, week, or month"

    if data["timeUnit"] == "month" and (
        not isinstance(data.get("month"), str) or not isinstance(data.get("year"), int)
    ):
        return "Month data must contain a month and year"

    return None


@api.post("/activities")
def create_activities():
    data = request.get_json(silent=True)
    error = validate_payload(data)

    if error:
        return make_response(error, 400)

    month = data.get("month") if data["timeUnit"] == "month" else None
    year = data.get("year") if data["timeUnit"] == "month" else None

    with models.session_scope() as session:
        external_id = generate_external_id()

        while session.scalar(
            select(models.Activities.id).where(
                models.Activities.external_id == external_id
            )
        ):
            external_id = generate_external_id()

        session.add(
            models.Activities(
                external_id=external_id,
                activities=data["activities"],
                chart_types=data["chartTypes"],
                time_unit=data["timeUnit"],
                month=month,
                year=year,
            )
        )

    return jsonify(external_id), 201


@api.get("/activities/<activities_id>")
def read_activities(activities_id):
    with models.session_scope() as session:
        activities = session.scalar(
            select(models.Activities).where(
                models.Activities.external_id == activities_id
            )
        )

        if activities is None:
            return make_response("Activities not found", 404)

        response = {
            "activities": decode_json_value(activities.activities),
            "chart_types": decode_json_value(activities.chart_types),
            "time_unit": activities.time_unit,
            "month": activities.month,
            "year": activities.year,
        }

    return jsonify(response)
