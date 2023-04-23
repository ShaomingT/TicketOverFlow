import uuid
import random
from datetime import datetime, timedelta
import json

# User entries
users = [
    {
        "id": "00000000-0000-0000-0000-000000000001",
        "name": "Ms. Jailyn Reichert MD",
        "email": "elbert@example.org"
    },
    {
        "id": "00000000-0000-0000-0000-000000000002",
        "name": "Mercedes Lockman",
        "email": "ashlee.cole@example.org"
    },
    {
        "id": "00000000-0000-0000-0000-000000000003",
        "name": "Marley Russel",
        "email": "athena.carroll@example.org"
    },
    {
        "id": "00000000-0000-0000-0000-000000000004",
        "name": "Mr. Cecil Zieme Sr.",
        "email": "calista@example.org"
    },
    {
        "id": "00000000-0000-0000-0000-000000000005",
        "name": "Marcus Hayes MD",
        "email": "deondre@example.org"
    },
    {
        "id": "00000000-0000-0000-0000-000000000006",
        "name": "Mckenzie Howell",
        "email": "pacocha@example.org"
    },
    {
        "id": "00000000-0000-0000-0000-000000000007",
        "name": "Bradford Stark",
        "email": "becker@example.org"
    },
    {
        "id": "00000000-0000-0000-0000-000000000008",
        "name": "Erick Hoeger",
        "email": "torrance.kris@example.org"
    },
    {
        "id": "00000000-0000-0000-0000-000000000009",
        "name": "Jewel Nitzsche",
        "email": "metz@example.org"
    },
    {
        "id": "00000000-0000-0000-0000-000000000010",
        "name": "Mr. Antwan Mraz I",
        "email": "sipes.cora@example.org"
    },
]

# Generate 10 random concerts
concerts = []
for _ in range(10):
    concert_id = str(uuid.uuid4())
    concerts.append({
        "id": concert_id,
        "name": f"Concert {_}",
        "venue": f"Venue {_}",
        "date": (datetime.now() + timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d'),
        "capacity": random.randint(100, 1000),
        "status": "ACTIVE",
    })

# Generate 10 random ticket entries
tickets = []
for _ in range(10):
    ticket_id = str(uuid.uuid4())
    concert = random.choice(concerts)
    user = random.choice(users)
    tickets.append({
        "id": ticket_id,
        "concert": {
            "id": concert["id"],
            "url": f"http://service_concert_service_concert_1:7777/api/v1/concerts/{concert['id']}"
        },
        "user": {
            "id": user["id"],
            "url": f"http://service_user_service_user_1:8888/api/v1/users/{user['id']}"
        },
        "print_status": "NOT_PRINTED"
    })

# Combine concerts and tickets in a single JSON object
combined_data = {
    "concerts": concerts,
    "tickets": tickets
}

with open("concerts.json", "w") as f:
    json.dump(concerts, f)

with open("tickets.json", "w") as f:
    json.dump(tickets, f)