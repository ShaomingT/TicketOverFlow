import json
from pymongo import MongoClient
import subprocess


print("restring container...")
subprocess.run(['docker-compose', 'down'], check=True)
subprocess.run(['docker-compose', 'up', '-d'], check=True)

print("loading data...")
# Read the JSON file
with open('users.json', 'r') as file:
    data = json.load(file)


# Connect to the MongoDB server
client = MongoClient('mongodb://root:example@localhost:27017/')

# Access the 'ticketoverflow' database and the 'users' collection
db = client.ticketoverflow
users_collection = db.users

print("inserting...")
# Insert the JSON data into the 'users' collection
result = users_collection.insert_many(data)

# Print the result
print(f"Inserted {len(result.inserted_ids)} documents into the 'users' collection.")
print("done.")