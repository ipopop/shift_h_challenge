import time
import schedule
import json
import os
from shiftheroes import ShiftHeroesAPI

def read_config_file(config_file):
    with open(config_file, "r") as file:
        config_data = json.load(file)
    return config_data.get("accounts", [])  # Return an empty list if "accounts" key is not present

def handle_reservation(api, planning_id):
    available_slots = api.list_available_slots(planning_id)

    if available_slots:
        first_slot_id = available_slots[0]['id']
        api.reserve_slot(planning_id, first_slot_id)
        print(f"Reservation successful for account with planning ID {planning_id}")
    else:
        print(f"No available slots found for account with planning ID {planning_id}")

def automate_slots_reservation(config_file):
    accounts = read_config_file(config_file)

    base_url = "https://shiftheroes.fr"  # The base URL from the existing "shiftheroes.py" code

    for account in accounts:
        planning_id = account.get("planning_id")
        if not planning_id:
            print(f"Planning ID not found for account {account}")
            continue

        api_key = os.getenv(f"API_KEY_{planning_id.upper()}")
        if not api_key:
            print(f"API key not found for account with planning ID {planning_id}")
            continue

        api = ShiftHeroesAPI(base_url, headers={'Authorization': f'Bearer {api_key}'})
        handle_reservation(api, planning_id)

if __name__ == "__main__":
    schedule.every(5).seconds.do(automate_slots_reservation, "config.json")

    while True:
        schedule.run_pending()
        time.sleep(1)
