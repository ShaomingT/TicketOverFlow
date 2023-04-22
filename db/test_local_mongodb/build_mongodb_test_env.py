import json
from pymongo import MongoClient
import subprocess


print("restarting container...")
subprocess.run(['docker-compose', 'down'], check=True)
subprocess.run(['docker-compose', 'up', '-d'], check=True)

print("loading data...")

# Connect to the MongoDB server
client = MongoClient('mongodb://root:example@localhost:27017/')

# Access the 'ticketoverflow' database and the 'users' collection
db = client.ticketoverflow

# Open the user data file and insert the data into the "users" collection
with open("test_data/users.json", "r") as f:
    user_data = json.load(f)
db["users"].insert_many(user_data)

# Open the ticket data file and insert the data into the "tickets" collection
# with open("test_data/tickets.json", "r") as f:
#     ticket_data = json.load(f)
# db["tickets"].insert_many(ticket_data)

# # Open the concert data file and insert the data into the "concerts" collection
# with open("test_data/concerts.json", "r") as f:
#     concert_data = json.load(f)
# db["concerts"].insert_many(concert_data)


# Print the result
# Print the number of documents inserted into the 'users' collection
print(f"Inserted {len(user_data)} documents into the 'users' collection.")
# print(f"Inserted {len(ticket_data)} documents into the 'tickets' collection.")
# print(f"Inserted {len(concert_data)} documents into the 'concerts' collection.")
print("done.")