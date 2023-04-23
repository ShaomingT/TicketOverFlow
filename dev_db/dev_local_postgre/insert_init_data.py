import json
from sqlalchemy import create_engine, text

# Define the PostgreSQL database URL
DB_URL = "postgresql://postgres:postgres@localhost:5432/ticketoverflow"

# Create a SQLAlchemy engine to connect to the "ticketoverflow" database
engine = create_engine(DB_URL)


# Read the JSON file
with open("users.json", "r") as f:
    data = json.load(f)

# Insert the JSON data into the "users" table
insert_user = text("""
    INSERT INTO users (id, name, email)
    VALUES (:id, :name, :email)
""")

with engine.connect() as conn:
    trans = conn.begin()  # Begin a new transaction
    try:
        for user in data:
            conn.execute(insert_user, {'id': user["id"], 'name': user["name"], 'email': user["email"]})
        trans.commit()  # Commit the transaction
    except Exception as e:
        print(f"Error: {e}")
        trans.rollback()  # Rollback the transaction in case of error