import requests

response=requests.get("https://jsonplaceholder.typicode.com/todos/1")

print(response.status_code)
print(response.json())

data=response.json()
print(data["title"])
print(data["completed"])
