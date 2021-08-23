import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect", allow_redirects=True)

first_redirect = response.history[0]
second_redirect = response.history[1]
third_redirect = response.history[2]

print(first_redirect.url)
print(second_redirect.url)
print(third_redirect.url)

print(response.url)
