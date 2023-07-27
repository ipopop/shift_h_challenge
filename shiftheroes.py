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
        Reserves a slot by sending a POST request to the API.

        Args:
            planning_id (int): The ID of the planning.
            slot_id (int): The ID of the slot to be reserved.

        Returns:
            Response: The response object returned by the API.
        """
        url = f"{self.base_url}/api/v1/plannings/{planning_id}/shifts/{slot_id}/reservations"
        response = requests.post(url, headers=self.headers)
        return response

    def quick_reservation(self, planning_id):
        """
        Performs a quick reservation of the first available slot for a given planning.

        Parameters:
            planning_id (int): The ID of the planning.

        Returns:
            Response: The response object returned by the API.
        """
        slots = self.get_planning_slots(planning_id)
        if len(slots) > 0:
            slot_id = slots[0]['id']
            return self.reserve_slot(planning_id, slot_id)
        else:
            raise Exception("No available slots for reservation.")


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

    response = api.quick_reservation(planning_id)
    print(f'Quick Reservation Response : {response}')
