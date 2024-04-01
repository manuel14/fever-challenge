import json
import requests
import unittest
from unittest.mock import patch

from api.events_api import app
from tests.mocked_responses import MOCKED_RESPONSE


API_URL = "https://provider.code-challenge.feverup.com/api/events"


class TestApp(unittest.TestCase):

    @patch('api.events_api.requests.get')
    def test_external_api_down(self, mock_get):
        # testing that cached is used if available when external api is down
        mock_get.side_effect = requests.exceptions.HTTPError
        with app.test_client() as client:
            response = client.get('/events')
            self.assertEqual(response.status_code, 200)

    def test_cached_response_used(self):
        client = app.test_client()
        with patch('api.events_api.requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.content = MOCKED_RESPONSE
            response1 = client.get(
                '/events?starts_at=2021-01-01T17:32:28&ends_at=2022-01-02T17:32:28')
            response2 = client.get(
                '/events?starts_at=2021-01-01T17:32:28&ends_at=2022-01-02T17:32:28')

            self.assertEqual(response1.status_code, 200)
            self.assertEqual(response2.status_code, 200)
            self.assertEqual(response1.data, response2.data)
            mock_get.assert_called_once()

    def test_no_results_for_params(self):
        client = app.test_client()
        with patch('api.events_api.requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.content = MOCKED_RESPONSE
            response = client.get(
                '/events?starts_at=2024-01-01T17:32:28&ends_at=2024-01-02T17:32:28')

            self.assertEqual(response.status_code, 200)
            expected_response = {
                "data": {
                    "events": []
                },
                "error": None
            }
            self.assertEqual(json.loads(response.data), expected_response)
            mock_get.assert_called_once()


if __name__ == '__main__':
    unittest.main()
