import json
import psycopg2
import os

# Environment variables from AWS Lambda configuration
DB_HOST = os.environ['DB_HOST']

DB_NAME = os.environ['DB_NAME']
DB_USER = os.environ['DB_USER']
DB_PASS = os.environ['DB_PASS']
DB_HOST = DB_HOST.split(":")[0]


def connect_to_db():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
    )
    return conn


# get ticket info from database
def get_ticket_info(ticket_id, conn):
    cur = conn.cursor()
    # get id, concert_id, user_id, print_status from tickets table, as well as concert_name, concert_date,
    # concert_venue from  concerts table, user_name, email from concerts and users table
    cur.execute(
        f"SELECT tickets.id, tickets.concert_id, tickets.user_id, tickets.print_status, concerts.name, concerts.date, concerts.venue, users.name, users.email FROM tickets INNER JOIN concerts ON tickets.concert_id = concerts.id INNER JOIN users ON tickets.user_id = users.id WHERE tickets.id = '{ticket_id}'", )
    ticket_info = cur.fetchone()
    # return the ticket info in a dictionary
    return {"id": ticket_id,
            "name": ticket_info[7],
            "email": ticket_info[8],
            "concert": {
                "id": ticket_info[1],
                "name": ticket_info[4],
                "date": ticket_info[5],
                "venue": ticket_info[6]
            }}


def get_concert_info(concert_id, conn):
    cur = conn.cursor()
    # get id, name, date, venue, max_seats, purchased_seats from concerts table
    # the purchase seats is calculated by summing the number of tickets purchased for each concert
    cur.execute(
        f"SELECT id, name, date, venue, capacity, (SELECT COUNT(*) FROM tickets WHERE concert_id = '{concert_id}') FROM concerts WHERE id = '{concert_id}'", )

    concert_info = cur.fetchone()
    # return the concert info in a dictionary
    return {"id": concert_id,
            "name": concert_info[1],
            "date": concert_info[2],
            "venue": concert_info[3],
            "seats": {
                "max": concert_info[4],
                "purchased": concert_info[5]
            }}


# the input {"event": "ticket",
#           "id": "[UUID]",}
def lambda_handler(event, context):
    try:
        body = json.loads(event["body"])
    except json.JSONDecodeError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({"error": f"Invalid JSON: {str(e)}"}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }

    event_name = body["event"]
    event_id = body["id"]

    # if the event is not "concert" or "ticket", return 404
    if event_name != "concert" and event_name != "ticket":
        return {
            'statusCode': 404,
            'body': json.dumps('Something happened')
        }
    conn = connect_to_db()

    # IF there is an error while no uuid is found, return 404
    try:
        if event_name == "ticket":
            ticket_info = get_ticket_info(event_id, conn)
            conn.close()
            return {
                'statusCode': 200,
                'body': json.dumps(ticket_info)
            }
        elif event_name == "concert":
            concert_info = get_concert_info(event_id, conn)
            conn.close()
            return {
                'statusCode': 200,
                'body': json.dumps(concert_info)
            }
    except Exception as e:
        # log the error in lambda
        print(e)
        return {
            'statusCode': 404,
            'body': json.dumps({"error": f"Invalid UUID: {str(e)}"}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
            
        
