import json
import requests
import unittest
from unittest.mock import patch

from api.main import app
from fastapi.testclient import TestClient
from tests.mocked_responses import MOCKED_RESPONSE


API_URL = "https://provider.code-challenge.feverup.com/api/events"
test_client = TestClient(app)


class TestApp(unittest.TestCase):

    @patch('api.main.requests.get')
    def test_external_api_down(self, mock_get):
        # Testing that cached response is used if available when external API is down
        mock_get.side_effect = requests.exceptions.RequestException

        response = test_client.get('/events')
        self.assertEqual(response.status_code, 200)

    def test_cached_response_used(self):
        with patch('api.main.requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.content = MOCKED_RESPONSE
            response1 = test_client.get(
                '/events?starts_at=2021-01-01T17:32:28&ends_at=2022-01-02T17:32:28')
            response2 = test_client.get(
                '/events?starts_at=2021-01-01T17:32:28&ends_at=2022-01-02T17:32:28')

            self.assertEqual(response1.status_code, 200)
            self.assertEqual(response2.status_code, 200)
            self.assertEqual(response1.content, response2.content)
            self.assertEqual(mock_get.call_count, 2)

    def test_no_results_for_params(self):
        with patch('api.main.requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.content = MOCKED_RESPONSE
            response = test_client.get(
                '/events?starts_at=2024-01-01T17:32:28&ends_at=2024-01-02T17:32:28')

            self.assertEqual(response.status_code, 200)
            expected_response = {
                "data": {
                    "events": []
                },
                "error": None
            }
            self.assertEqual(json.loads(response.content), expected_response)
            mock_get.assert_called_once()


if __name__ == '__main__':
    unittest.main()
