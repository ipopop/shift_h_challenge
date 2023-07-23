import requests

headers = {
  'Authorization': 'Bearer b1869acc141e5f20c87dcbac8b9a3e9d',
}

# GET Plannings List
response = requests.get('https://shiftheroes.fr/api/v1/plannings', headers=headers)

plannings_list = response.json()

# Print Plannings List
print(f'Plannings List : {plannings_list}')

# GET Plannings List ID
planning_id = (plannings_list[2]['id'])

# Print Planning ID
print(f'Planning ID : {planning_id}')

# GET Planning Slots
planning_slots = requests.get('https://shiftheroes.fr/api/v1/plannings/' + planning_id + '/shifts', headers=headers)

# Print Planning Slots
print(f'Planning Slots : {planning_slots.json()}')

# Print Planning Slots ID 
print(f'Planning Slots ID : {planning_slots.json()[2]["id"]}')

slot_id = planning_slots.json()[2]['id']

# POST Planning Slots ID
response3 = requests.post('https://shiftheroes.fr/api/v1/plannings/' + planning_id + '/shifts/' + slot_id + '/reservations', headers=headers)

# POST /api/v1/plannings/VezfK6/shifts/6JFOGj/reservations

# Print Planning Slots ID Reservation 
print(f'Planning Slots ID Reservation : {response3}')
# print(response3.json()[2]['id'])