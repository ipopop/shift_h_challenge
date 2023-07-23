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
        url = f"{self.base_url}/api/v1/plannings"
        response = requests.get(url, headers=self.headers)
        return response.json()
    
    def get_planning_slots(self, planning_id):
        url = f"{self.base_url}/api/v1/plannings/{planning_id}/shifts"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def reserve_slot(self, planning_id, slot_id):
        url = f"{self.base_url}/api/v1/plannings/{planning_id}/shifts/{slot_id}/reservations"
        response = requests.post(url, headers=self.headers)
        return response

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

    planning_slots = api.get_planning_slots(planning_id)
    print(f'Planning Slots : {planning_slots}')

    slot_id = planning_slots[2]['id']
    response = api.reserve_slot(planning_id, slot_id)
    print(f'Planning Slots ID Reservation : {response}')
