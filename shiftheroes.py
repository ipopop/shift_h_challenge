import requests

# GET Plannings List
headers = {
  'Authorisation': 'Bearer b1869acc141e5f20c87dcbac8b9a3e9d',
}
response = requests.get('https://shiftheroes.fr/api/v1/plannings', headers=headers)
planning_id = response.json()[2]['id']

# GET Planning Slots
response = requests.get('https://shiftheroes.fr/api/v1/plannings/' + planning_id + '/shifts', headers=headers)
print(response.json())

