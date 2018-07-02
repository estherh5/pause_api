import json
import random
import string

from flask import jsonify, make_response, request
from sqlalchemy.orm.exc import NoResultFound

from pause import models


def create_activities():
    # Request should contain:
    # activities <dict>
    # chartTypes <dict>
    # timeUnit <str>
    # month <str> (optional)
    # year <int> (optional)
    data = request.get_json()

    # Return error if request is missing data
    if (not data or 'activities' not in data or 'chartTypes' not in data or
        'timeUnit' not in data):
            return make_response(
                'Request must contain activities and time unit', 400)

    # Return error if activities is not a dictionary
    if not isinstance(data['activities'], dict):
        return make_response('Activities must be a dictionary', 400)

    # Return error if chartTypes is not a dictionary
    if not isinstance(data['chartTypes'], dict):
        return make_response('Chart types must be a dictionary', 400)

    # Return error if timeUnit is not a string
    if not isinstance(data['timeUnit'], str):
        return make_response('Time unit must be a string', 400)

    if data['timeUnit'] == 'month':
        month = data['month']
        year = data['year']

    else:
        month = None
        year = None

    # Generate random external id for activities
    external_id = ''.join(
        random.choices(string.ascii_letters + string.digits, k=16))

    # Connect to database
    session = models.Session()

    # Add activities to database
    activities = models.Activities(
        external_id=external_id,
        activities=json.dumps(data['activities']),
        chart_types=json.dumps(data['chartTypes']),
        time_unit=data['timeUnit'],
        month=month,
        year=year
        )

    session.add(activities)

    session.commit()

    session.close()

    return make_response(external_id, 201)


def read_activities(activities_id):
    # Connect to database
    session = models.Session()

    # Retrieve activities from database
    try:
        activities = session.query(models.Activities).with_entities(
            models.Activities.activities, models.Activities.chart_types,
            models.Activities.time_unit, models.Activities.month,
            models.Activities.year).filter(
            models.Activities.external_id == activities_id).limit(1).one()

        session.close()

        activities = activities._asdict()

        # Convert JSON data to dictionary
        activities['activities'] = json.loads(activities['activities'])
        activities['chart_types'] = json.loads(activities['chart_types'])

        return jsonify(activities)

    # Return error if activities not returned from query
    except NoResultFound:
        session.close()

        return make_response('Activities not found', 404)
