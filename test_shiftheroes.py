import unittest
from unittest.mock import MagicMock, patch
from shiftheroes import ShiftHeroesAPI


class TestShiftHeroesAPI(unittest.TestCase):
    def setUp(self):
        """
        Set up the necessary variables and objects for the test case.

        This function initializes the base URL, headers, and ShiftHeroesAPI object
        for the test case. It should be called before each test.

        Parameters:
            self (TestClass): The test case object.

        Returns:
            None
        """
        self.base_url = "https://shiftheroes.fr"
        self.headers = {
            'Authorization': 'Bearer secret_bearer_code',
        }
        self.api = ShiftHeroesAPI(self.base_url, self.headers)

    def test_get_plannings(self):
        """
        Test the 'get_plannings' function.

        This function is responsible for testing the 'get_plannings' function of the API class.
        It checks if the function correctly returns the expected response.

        Parameters:
            self: The current instance of the test class.

        Returns:
            None
        """
        expected_response = [{'id': 'X05fB9', 'planning_type': 'daily', 'state': 'available', 'published_at': '2023-07-22T16:00:28.724Z'}, {'id': 'VezfK6', 'planning_type': 'permanent',
                                                                                                                                            'state': 'available', 'published_at': '2023-07-21T16:35:51.522Z'}, {'id': 'O1oflz', 'planning_type': 'weekly', 'state': 'available', 'published_at': '2023-07-20T13:40:21.779Z'}]

        with patch('requests.get') as mock_get:
            mock_get.return_value.json.return_value = expected_response
            response = self.api.get_plannings()

        self.assertEqual(response, expected_response)

    def test_get_planning_slots(self):
        """
        Test the get_planning_slots function.

        Parameters:
            self (TestClassName): The current test class.

        Returns:
            None
        """
        planning_id = 'O1oflz'
        expected_response = [{'id': 'xZGFwL', 'day': 'lundi', 'start_hour': '2000-01-01T08:00:00.000Z',
                              'end_hour': '2000-01-01T14:00:00.000Z', 'seats': 14, 'seats_taken': 14}]

    def test_reserve_slot(self):
        """
        Test the 'reserve_slot' function.

        This function is responsible for testing the 'reserve_slot' function of the API class.
        It checks if the function correctly handles successful and unsuccessful reservations.

        Parameters:
            self: The current instance of the test class.

        Returns:
            None
        """
        # Create a mock response object for a successful reservation (status code: 201)
        mock_response = MagicMock()
        mock_response.status_code = 201

        # Patch the 'requests.post' method to return the mock response
        with patch('requests.post') as mock_post:
            mock_post.return_value = mock_response

            # Make the reservation and check if the response is as expected
            response = self.api.reserve_slot('planning_id', 'slot_id')
            self.assertEqual(response, mock_response)

            # Now, let's test the case when the reservation fails (status code: anything other than 201)
            # Create a mock response object for an unsuccessful reservation (status code: 400)
            mock_response_fail = MagicMock()
            mock_response_fail.status_code = 400

            # Patch the 'requests.post' method again to return the new mock response
            with patch('requests.post') as mock_post_fail:
                mock_post_fail.return_value = mock_response_fail

                # Make the reservation and check if it raises an Exception as expected
                with self.assertRaises(Exception):
                    self.api.reserve_slot('planning_id', 'slot_id')

