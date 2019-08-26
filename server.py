import os

from flask import Flask, jsonify, request
from flask_cors import CORS

from pause import pause

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
if os.environ['ENV_TYPE'] == 'Dev':
    app.config['DEBUG'] = True


@app.route('/api/pause/activities', methods=['POST'])
def pause_activities():
    # Post Pause activities data when client sends the jsonified activities,
    # chart types, time unit, month, and year in the request body; no bearer
    # token needed
    if request.method == 'POST':
        return pause.create_activities()


@app.route('/api/pause/activities/<activities_id>', methods=['GET'])
def pause_activities_id(activities_id):
    # Get Pause activities data when client sends the activities id in the
    # request URL; no bearer token needed
    if request.method == 'GET':
        return pause.read_activities(activities_id)
