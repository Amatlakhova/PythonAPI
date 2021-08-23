import requests

#1
response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type")

print(response.text)
print(response.status_code)

#2
method = {"method": "HEAD"}
response = requests.head("https://playground.learnqa.ru/ajax/api/compare_query_type", data= method)

print(response.text)
print(response.status_code)

#3
method = {"method": "DELETE"}
response = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", data= method)

print(response.text)
print(response.status_code)

#4
url = "https://playground.learnqa.ru/ajax/api/compare_query_type"

map = [
    {"method": "GET"},
    {"method": "POST"},
    {"method": "PUT"},
    {"method": "DELETE"}
]

for data in map:

    print(requests.get(url, params= data).text)
    requests.get(url, params= data)
    print(requests.post(url, data= data).text)
    requests.post(url, data= data)
    print(requests.put(url, data=data).text)
    requests.put(url, data=data)
    print(requests.delete(url, data=data).text)
    requests.delete(url, data=data)

