import json

from utils.tests import PauseTestCase


# Test /api/pause/activities endpoint [POST, GET]
class TestActivities(PauseTestCase):
    def test_activities_post_and_get_day_data(self):
        # Arrange
        activities = {'0': {'id': 0, 'value': 24, 'label': 'test'}}
        chart_types = {'0': 'pie'}
        time_unit = 'day'

        data = {
            'activities': activities,
            'chartTypes': chart_types,
            'timeUnit': time_unit
        }

        # Act [POST]
        post_response = self.client.post(
            '/api/pause/activities',
            data=json.dumps(data),
            content_type='application/json'
            )
        activities_id = post_response.get_data(as_text=True)

        # Assert [POST]
        self.assertEqual(post_response.status_code, 201)

        # Act [GET]
        get_response = self.client.get(
            '/api/pause/activities/' + activities_id
            )
        activities_data = json.loads(get_response.get_data(as_text=True))

        # Assert [GET]
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(activities_data['activities'], activities)
        self.assertEqual(activities_data['chart_types'], chart_types)
        self.assertEqual(activities_data['time_unit'], time_unit)

    def test_activities_post_data_error(self):
        # Act
        post_response = self.client.post(
            '/api/pause/activities'
            )
        error = post_response.get_data(as_text=True)

        # Assert
        self.assertEqual(post_response.status_code, 400)
        self.assertEqual(
            error, 'Request must contain activities and time unit')

    def test_activities_post_activities_error(self):
        # Arrange
        activities = [{'id': 0, 'value': 24, 'label': 'test'}]
        chart_types = {'0': 'pie'}
        time_unit = 'day'

        data = {
            'activities': activities,
            'chartTypes': chart_types,
            'timeUnit': time_unit
        }

        # Act [POST]
        post_response = self.client.post(
            '/api/pause/activities',
            data=json.dumps(data),
            content_type='application/json'
            )
        error = post_response.get_data(as_text=True)

        # Assert
        self.assertEqual(post_response.status_code, 400)
        self.assertEqual(error, 'Activities must be a dictionary')

    def test_activities_post_chart_types_error(self):
        # Arrange
        activities = {'0': {'id': 0, 'value': 24, 'label': 'test'}}
        chart_types = ['pie']
        time_unit = 'day'

        data = {
            'activities': activities,
            'chartTypes': chart_types,
            'timeUnit': time_unit
        }

        # Act [POST]
        post_response = self.client.post(
            '/api/pause/activities',
            data=json.dumps(data),
            content_type='application/json'
            )
        error = post_response.get_data(as_text=True)

        # Assert
        self.assertEqual(post_response.status_code, 400)
        self.assertEqual(error, 'Chart types must be a dictionary')

    def test_activities_post_time_unit_error(self):
        # Arrange
        activities = {'0': {'id': 0, 'value': 24, 'label': 'test'}}
        chart_types = {'0': 'pie'}
        time_unit = ['day']

        data = {
            'activities': activities,
            'chartTypes': chart_types,
            'timeUnit': time_unit
        }

        # Act [POST]
        post_response = self.client.post(
            '/api/pause/activities',
            data=json.dumps(data),
            content_type='application/json'
            )
        error = post_response.get_data(as_text=True)

        # Assert
        self.assertEqual(post_response.status_code, 400)
        self.assertEqual(error, 'Time unit must be a string')

    def test_activities_post_and_get_month_data(self):
        # Arrange
        activities = {'0': {'id': 0, 'value': 24, 'label': 'test'}}
        chart_types = {'0': 'pie'}
        time_unit = 'month'
        month = 'January'
        year = 2018

        data = {
            'activities': activities,
            'chartTypes': chart_types,
            'timeUnit': time_unit,
            'month': month,
            'year': year
        }

        # Act [POST]
        post_response = self.client.post(
            '/api/pause/activities',
            data=json.dumps(data),
            content_type='application/json'
            )
        activities_id = post_response.get_data(as_text=True)

        # Assert [POST]
        self.assertEqual(post_response.status_code, 201)

        # Act [GET]
        get_response = self.client.get(
            '/api/pause/activities/' + activities_id
            )
        activities_data = json.loads(get_response.get_data(as_text=True))

        # Assert [GET]
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(activities_data['activities'], activities)
        self.assertEqual(activities_data['chart_types'], chart_types)
        self.assertEqual(activities_data['time_unit'], time_unit)
        self.assertEqual(activities_data['month'], month)
        self.assertEqual(activities_data['year'], year)

    def test_activities_get_not_found(self):
        # Arrange
        external_id = 'test'

        # Act
        get_response = self.client.get(
            '/api/pause/activities/' + external_id
            )
        error = get_response.get_data(as_text=True)

        # Assert
        self.assertEqual(get_response.status_code, 404)
        self.assertEqual(error, 'Activities not found')
