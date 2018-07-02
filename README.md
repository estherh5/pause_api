[![Build Status](https://travis-ci.org/estherh5/pause_api.svg?branch=master)](https://travis-ci.org/estherh5/pause_api)
[![codecov](https://codecov.io/gh/estherh5/pause_api/branch/master/graph/badge.svg)](https://codecov.io/gh/estherh5/pause_api)

# Pause
[Pause](https://pause.crystalprism.io/) is a [React](https://reactjs.org/) web app that allows you to plan your day, week or month and visually display each day's breakdown of 24 hours in a chart generated with [React-ChartJS-2](http://jerairrest.github.io/react-chartjs-2/). You can enter any activities you would like in a table, including the activity name and the number of hours you would like to dedicate to that activity. Each chart updates dynamically whenever you add, delete, or update an activity. You can toggle between different chart types (pie, bar, radar, doughnut) to visualize your data in different ways. Chart color palettes are generated randomly with a modified version of [PleaseJS](https://github.com/Fooidge/PleaseJS). A table beneath the chart calculates how many hours you will spend on each activity weekly, monthly, and yearly, as well as how many hours you will spend on each activity in your remaining lifespan based on your current age and your specified ending age. If you are not sure which activities to start with, you can click one of the starter buttons to display activities for common lifestyles. You can store your activities using the API built here, which generates a unique external identifier that you can use to access your activities in a URL (i.e., `https://pause.crystalprism.io/<external_id>`), allowing you to revisit them and share them with others.

## Setup
1. Clone this repository on your server.
2. Install requirements by running `pip install -r requirements.txt`.
3. Create a PostgreSQL database to store Pause activities data, as well as a user that has all privileges on your database.
4. Set the following environment variables for the API:
    * `FLASK_APP` for the Flask application name for your server ("server.py")
    * `ENV_TYPE` for the environment status (set this to "Dev" for testing or "Prod" for live)
    * `DB_CONNECTION` for the [database URL](http://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls) to connect to your database via SQLAlchemy ORM (i.e., '<dialect+driver://username:password@host:port/database>')
    * `DB_NAME` for the name of your database
5. Load the initial database structure by running `alembic upgrade head`.
    * Note that you might need to add `PYTHONPATH=.` to the beginning of your revision command if Alembic can't find your module.
6. Start the server by running `flask run` (if you are making changes while the server is running, enter `flask run --reload` instead for instant updates).

## API
To post and retrieve data for Pause activities, a client can send a request to the following endpoints. Activities data gets saved in the database table "activities" (optional fields are denoted with an asterisk):
<p align="center"><img title="Pause Database" src ="images/pause-database.png" /></p>

\
**POST** /api/pause/activities
* Post activities data by sending the jsonified activities, chart types, time unit, month, and year in the request body. No bearer token is needed in the request Authorization header.
* Example request body:
```javascript
{
    "activities": {
        "0": [
            {
                "id": 0,
                "label": "",
                "value": 0
            },
            {
                "color": "#ff6300",
                "id": 1,
                "label": "sleep",
                "value": 8
            },
            {
                "color": "#daff00",
                "id": 2,
                "label": "breakfast",
                "value": 0.25
            },
            {
                "color": "#1bff00",
                "id": 3,
                "label": "class",
                "value": 6
            },
            {
                "color": "#00ffa3",
                "id": 4,
                "label": "lunch",
                "value": 0.5
            },
            {
                "color": "#009bff",
                "id": 5,
                "label": "homework",
                "value": 3
            },
            {
                "color": "#2400ff",
                "id": 6,
                "label": "dinner",
                "value": 0.5
            },
            {
                "color": "#e300ff",
                "id": 7,
                "label": "studying",
                "value": 4
            },
            {
                "color": "#ff005b",
                "id": 8,
                "label": "relax",
                "value": 1.75
            }
        ]
    },
    "chart_types": {
        "0": "pie"
    },
    "month": null,
    "time_unit": "day",
    "year": null
}
```

\
**GET** /api/pause/activities/[activities_id]
* Retrieve activities data by sending the activities id in the request URL. No bearer token is needed in the request Authorization header.
* Example response body:
```javascript
{
    "activities": {
        "0": [
            {
                "id": 0,
                "label": "",
                "value": 0
            },
            {
                "color": "#ff003d",
                "id": 1,
                "label": "sleep",
                "value": 8
            },
            {
                "color": "#ff9d00",
                "id": 2,
                "label": "breakfast",
                "value": 0.5
            },
            {
                "color": "#86ff00",
                "id": 3,
                "label": "work",
                "value": 8
            },
            {
                "color": "#00ff54",
                "id": 4,
                "label": "lunch",
                "value": 0.5
            },
            {
                "color": "#00ceff",
                "id": 5,
                "label": "working out",
                "value": 1
            },
            {
                "color": "#0b00ff",
                "id": 6,
                "label": "dinner",
                "value": 0.5
            },
            {
                "color": "#e600ff",
                "id": 7,
                "label": "relaxing",
                "value": 5.5
            }
        ]
    },
    "chart_types": {
        "0": "pie"
    },
    "month": null,
    "time_unit": "day",
    "year": null
}
```
