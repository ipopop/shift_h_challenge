import time
import datetime
import requests
import threading
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the bearer code from the environment variable
secret_bearer_code = os.getenv("SECRET_BEARER_CODE_001")


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
        response_json = response.json()
        if "error" in response_json:
            raise Exception(f"Failed to get planning slots. Error: {response_json['error']}")
        return response_json

    def reserve_slot(self, planning_id, slot_id):
        """
        Performs a reservation of a slot for a given planning.

        Parameters:
            planning_id (str): The ID of the planning.
            slot_id (str): The ID of the slot.

        Returns:
            Response: The response object returned by the API.
        """
        url = f"{self.base_url}/api/v1/plannings/{planning_id}/shifts/{slot_id}/reservations"
        response = requests.post(url, headers=self.headers)

        if response.status_code == 201:
            return response
        else:
            raise Exception(
                f"Failed to reserve slot. Response code: {response.status_code}")

    def list_available_slots(self, planning_id):
        planning_slots = self.get_planning_slots(planning_id)
        print(f"Planning Slots: {planning_slots}")
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


def check_and_reserve_available_slots(planning_id):
    """
    Checks for available slots and reserves them.

    This function repeatedly checks for available slots by calling the `list_available_slots` method. If an available slot is found, it reserves the slot by calling the `reserve_slot` method. The function also prints diagnostic messages indicating the progress of the slot checking and reservation process.

    Parameters:
        planning_id (str): The ID of the planning.

    Returns:
        None
    """
    count_slots_reserved = 0
    start_time = None

    while count_slots_reserved < 14:
        if start_time is None:
            plannings = api.get_plannings()
            planning = next((p for p in plannings if p["id"] == planning_id), None)
            if planning and planning["state"] == "published":
                start_time = time.time()
                print(f"[{datetime.datetime.now()}] Planning is published. Starting reservation process...")
            else:
                print(f"[{datetime.datetime.now()}] Planning is not published yet. Waiting...")
                time.sleep(1)
                continue

        if start_time is not None and (time.time() - start_time) > 10:
            print(f"[{datetime.datetime.now()}] Reservation process did not start within 10 seconds.")
            break

        available_slots = api.list_available_slots(planning_id)
        print(f"[{datetime.datetime.now()}] Checking for available slots...")
        print(f"Available Slots : {available_slots}")

        if available_slots:
            for slot in available_slots:
                slot_id = slot["id"]
                try:
                    api.reserve_slot(planning_id, slot_id)
                    count_slots_reserved += 1
                    print(f"[{datetime.datetime.now()}] Slot {slot_id} reserved successfully.")
                except Exception as e:
                    print(f"[{datetime.datetime.now()}] Failed to reserve slot {slot_id}: {str(e)}")

        time.sleep(1)  # Wait for 1 second before checking again

    if count_slots_reserved == 14:
        print(f"[{datetime.datetime.now()}] Successfully reserved 14 slots.")
    else:
        print(f"[{datetime.datetime.now()}] Reservation process stopped.")


def check_planning(planning_id):
    print(f"Checking planning ID: {planning_id}")
    check_and_reserve_available_slots(planning_id)


if __name__ == "__main__":
    base_url = "https://shiftheroes.fr"
    headers = {
        "Authorization": f"Bearer {secret_bearer_code}"
    }

    api = ShiftHeroesAPI(base_url, headers)
    plannings = api.get_plannings()
    print(f"Plannings List : {plannings}")

    # Choose the planning type to reserve slots
    desired_planning_type = "daily"

    found_planning_ids = []  # List to store the planning IDs that match the desired planning type

    # Iterate over all the plannings
    for planning in plannings:
        if planning["planning_type"] == desired_planning_type:
            planning_id = planning["id"]
            found_planning_ids.append(planning_id)
            print(f"Selected planning ID: {planning_id}")

    if not found_planning_ids:
        print(f"No planning found with planning type '{desired_planning_type}'")
    else:
        # Create a separate thread for each planning and start them concurrently
        threads = []
        for planning_id in found_planning_ids:
            thread = threading.Thread(target=check_planning, args=(planning_id,))
            threads.append(thread)
            thread.start()

        # Wait for all the threads to finish
        for thread in threads:
            thread.join()