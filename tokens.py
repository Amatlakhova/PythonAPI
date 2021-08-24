import requests
import json
import time

# Create a task
response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")
data = json.loads(response.text)
token = data['token']
seconds = data['seconds']
print(response.text)

# Request with Token
params = {"token": token}
response1 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params= params)
print(response1.text)

# Check status is correct
data = json.loads(response1.text)
status = data['status']

if 'Job is NOT ready' == status:
    print(f"Correct status")
else:
    print(status)

# Wait seconds
time.sleep(seconds)

# Request with Token
response2 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params= params)
print(response2.text)

# Check status is correct
data = json.loads(response2.text)
new_status = data['status']
result = data['result']

if 'Job is ready' == new_status:
    print(f"Correct status")
else:
    print(new_status)

# Check result received
if result is not None:
    print(f"Result received: {result}")
else:
    print(f"Result is {result} - not correct!")


