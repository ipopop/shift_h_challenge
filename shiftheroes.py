import time
import datetime
import requests
import os
from dotenv import load_dotenv
import schedule

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

    def list_available_slots(self, planning_id):
        """
        List the available slots for a given planning ID.

        Parameters:
            planning_id (str): The ID of the planning.

        Returns:
            list: A list of available slots.
        """
        planning_slots = self.get_planning_slots(planning_id)
        available_slots = []

        for slot in planning_slots:
            start_time_str = slot["start_hour"]
            end_time_str = slot["end_hour"]

            start_time = datetime.datetime.fromisoformat(start_time_str[:-1])  # Remove 'Z' at the end
            end_time = datetime.datetime.fromisoformat(end_time_str[:-1])  # Remove 'Z' at the end

            # Check if the slot is available and starts in the future
            if slot["seats_taken"] < slot["seats"] and start_time > datetime.datetime.now():
                slot_info = {
                    "id": slot["id"],
                    "day": slot["day"],
                    "start_time": start_time,
                    "end_time": end_time,
                    "seats_available": slot["seats"] - slot["seats_taken"]
                }
                available_slots.append(slot_info)

        return available_slots
    
def print_countdown(count):
    for i in range(count, 0, -1):
        print(f'[{datetime.datetime.now()}] Function is starting from {i} seconds...', flush=True)
        time.sleep(1)
    
def check_and_reserve_available_slots():
    """
    Checks for available slots and reserves the first one.

    This function repeatedly checks for available slots by calling the `list_available_slots` method of the `api` object. If an available slot is found, it reserves the first one by calling the `reserve_slot` method of the `api` object. The function also prints diagnostic messages indicating the progress of the slot checking and reservation process.

    Parameters:
        None

    Returns:
        None
    """
    count_no_slots = 0  # Counter for "Available Slots : []"

    while True:
        available_slots = api.list_available_slots(planning_id)
        print(f'[{datetime.datetime.now()}] Checking for available slots...')
        print(f'Available Slots : {available_slots}')

        if available_slots:
            first_slot_id = available_slots[0]['id']
            print(f'First Slot ID : {first_slot_id}')

            api.reserve_slot(planning_id, first_slot_id)
            print("Reservation successful!")
            
            schedule.clear('check_and_reserve_available_slots')
            break
        else:
            count_no_slots += 1

        time.sleep(5)

    print(f'No available slots found after {count_no_slots} checks.')


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

    available_slots = api.list_available_slots(planning_id)
    print(f'Available Slots : {available_slots}')

    if available_slots:
        first_slot_id = available_slots[0]['id']
        print(f'First Slot ID : {first_slot_id}')

        # Make a quick reservation for the first available slot
        api.reserve_slot(planning_id, first_slot_id)
        print("Reservation successful!")
    else:
        print("No available slots found.")

    schedule.every(5).seconds.do(check_and_reserve_available_slots)
    
    while True:
        schedule.run_pending()
        time.sleep(1)
