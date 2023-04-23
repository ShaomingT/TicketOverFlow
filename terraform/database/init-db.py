import json
import psycopg2
import sys

db_host = sys.argv[1]
db_name = sys.argv[2]
db_user = sys.argv[3]
db_password = sys.argv[4]
json_file = sys.argv[5]

# extract the last four digit after ':' of db_host as the db_host
db_host = db_host.split(":")[0]

# Read the JSON data
with open(json_file, "r") as f:
    data = json.load(f)

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host=db_host,
    dbname=db_name,
    user=db_user,
    password=db_password
)

print("init tables..")
# execute the sql file init-db.sql to create the table
with conn.cursor() as cursor:
    with open("./database/init-db.sql", "r") as f:
        cursor.execute(f.read())
    conn.commit()

#todo: downlaod the latest data

print("insert data..")
# Insert the JSON data into the database
sql_str = ""
with conn.cursor() as cursor:
    for entry in data:
        # insert id, name email from entry to the database
        sql_str += "INSERT INTO users (id, name, email) VALUES ('{}', '{}', '{}'); \n".format(entry["id"], entry["name"], entry["email"])
    print(sql_str)
    cursor.execute(sql_str)
    conn.commit()

conn.close()
