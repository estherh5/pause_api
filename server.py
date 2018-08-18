import os
import requests

from bs4 import BeautifulSoup
from flask import Flask, jsonify, request
from flask_cors import CORS

from pause import pause

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
if os.environ['ENV_TYPE'] == 'Dev':
    app.config['DEBUG'] = True


@app.route('/api/marian/image/<symbol>/<article_id>', methods=['GET'])
def stock_image(symbol, article_id):
    if request.method == 'GET':
        article_url = ('https://api.iextrading.com/1.0/stock/' + symbol +
            '/article/' + article_id)

        article_html = requests.get(article_url)

        html_content = article_html.content

        article_soup = BeautifulSoup(html_content, 'html.parser')

        image = article_soup.find(property='og:image').get('content')

        return jsonify(image)


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
