import requests


LOCAL_API_URL = {
    "user": "http://localhost:8888/api/v1/users",
    "ticket": "http://localhost:9999/api/v1/tickets",
    "concert":  "http://localhost:7777/api/v1/concerts",
    "hamilton": "http://localhost:6666/api/v1/hamilton"
}

# get all concerts
response = requests.get(LOCAL_API_URL["concert"])
res = response.json()
for i in res:
    # visit hamilton service to generate svg
    url = LOCAL_API_URL["hamilton"] + "/concerts/" + i["id"]
    print(url)
    response = requests.post(url, json={})
    print(response.json())

