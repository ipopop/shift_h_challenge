import unittest
from unittest.mock import MagicMock, patch
from shiftheroes import ShiftHeroesAPI

class TestShiftHeroesAPI(unittest.TestCase):
    def setUp(self):
        self.base_url = "https://shiftheroes.fr"
        self.headers = {
            'Authorization': 'Bearer secret_bearer_code',
        }
        self.api = ShiftHeroesAPI(self.base_url, self.headers)

    def test_get_plannings(self):
        expected_response = [{'id': 'X05fB9', 'planning_type': 'daily', 'state': 'available', 'published_at': '2023-07-22T16:00:28.724Z'}, {'id': 'VezfK6', 'planning_type': 'permanent', 'state': 'available', 'published_at': '2023-07-21T16:35:51.522Z'}, {'id': 'O1oflz', 'planning_type': 'weekly', 'state': 'available', 'published_at': '2023-07-20T13:40:21.779Z'}]
        
        with patch('requests.get') as mock_get:
            mock_get.return_value.json.return_value = expected_response
            response = self.api.get_plannings()
        
        self.assertEqual(response, expected_response)

    def test_get_planning_slots(self):
        planning_id = 'O1oflz'
        expected_response = [{'id': 'xZGFwL', 'day': 'lundi', 'start_hour': '2000-01-01T08:00:00.000Z', 'end_hour': '2000-01-01T14:00:00.000Z', 'seats': 14, 'seats_taken': 14}]

