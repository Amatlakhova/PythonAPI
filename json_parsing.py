import requests

response = requests.post("https://playground.learnqa.ru/api/get_301", allow_redirects=True)
first_redirect = response.history[0]
second_redirect = response

print(first_redirect.url)
print(second_redirect.url)


