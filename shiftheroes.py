import time
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the bearer code from the environment variable
secret_bearer_code = os.getenv("SECRET_BEARER_CODE")


class ShiftHeroesAPI:
    def __init__(self, base_url, headers):
        self.base_url = base_url
        self.headers = headers

    def get_plannings(self):
        """
        Retrieves a list of plannings from the server.

        :return: A JSON object containing the plannings.
        """
        url = f"{self.base_url}/api/v1/plannings"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_planning_slots(self, planning_id):
        """
        Get the planning slots for a given planning ID.

        Parameters:
            planning_id (int): The ID of the planning.

        Returns:
            dict: The planning slots in JSON format.
        """
        url = f"{self.base_url}/api/v1/plannings/{planning_id}/shifts"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def reserve_slot(self, planning_id, slot_id):
        """
        Performs a quick reservation of the first available slot for a given planning.

        Parameters:
            planning_id (str): The ID of the planning.

        Returns:
            Response: The response object returned by the API.
        """
        url = "{}/api/v1/plannings/{}/shifts/{}/reservations".format(
            self.base_url, planning_id, slot_id)
        response = requests.post(url, headers=self.headers)

        if response.status_code == 201:
            return response
        else:
            raise Exception(
                "Failed to reserve slot. Response code: {}".format(response.status_code))

    # TODO : list available slots on a daily or weekly schedule less than 5 seconds after publication
    # new code here...


if __name__ == "__main__":
    base_url = "https://shiftheroes.fr"
    headers = {
        'Authorization': f'Bearer {secret_bearer_code}',
    }

    api = ShiftHeroesAPI(base_url, headers)
    plannings = api.get_plannings()
    print(f'Plannings List : {plannings}')

    planning_id = plannings[2]['id']
    print(f'Planning ID : {planning_id}')
