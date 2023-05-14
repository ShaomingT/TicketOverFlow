import json
import subprocess
import os
import psycopg2
import json

# Environment variables from AWS Lambda configuration
DB_HOST = os.environ['DB_HOST']
DB_NAME = os.environ['DB_NAME']
DB_USER = os.environ['DB_USER']
DB_PASS = os.environ['DB_PASS']
DB_HOST = DB_HOST.split(":")[0]

INPUT_PATH = "/tmp"
OUTPUT_PATH = "/tmp"
HAMILTON_PATH = "./bin/hamilton-v1.1.0-linux-amd64"


# DB_HOST = "terraform-20230423124358945300000001.cvwf3fikf7zu.us-east-1.rds.amazonaws.com"
# DB_NAME = "ticketoverflow"
# DB_USER = "postgres"
# DB_PASS = "postgres"
# HAMILTON_PATH = "./bin/hamilton-v1.1.0-darwin-arm64"


def connect_to_db():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
    )
    return conn


def exec_hamilton(cmd):
    print(">> start exec hamilton")
    try:
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
        print(">> Output:", output.decode('utf-8'))
    except subprocess.CalledProcessError as e:
        print(">> Error output:", e.output.decode('utf-8'))
        raise e

    print(">> hamilton finished")


def handler_ticket(ticket_input, conn):
    ticket_id = ticket_input["id"]
    input_path = f"{INPUT_PATH}/{ticket_id}.json"
    output_path = f"{OUTPUT_PATH}/{ticket_id}"

    print(f">> ticket id: {ticket_id}")
    print(f">> input path: {input_path}")
    print(f">> output path: {output_path}")

    # dump input to file
    with open(input_path, "w") as f:
        json.dump(ticket_input, f)

    cmd = f"{HAMILTON_PATH} generate ticket --input {input_path} --output {output_path}"

    # run exec_hamilton
    exec_hamilton(cmd)

    with open(f"{output_path}.svg", "r") as f:
        svg_content = f.read()

    # write svg_content to svg field in table tickets
    cur = conn.cursor()
    cur.execute(f"UPDATE tickets SET svg = '{svg_content}' WHERE id = '{ticket_id}'")
    # change the print_Status to "PRINTED"
    cur.execute(f"UPDATE tickets SET print_status = 'PRINTED' WHERE id = '{ticket_id}'")
    conn.commit()
    conn.close()
    return {
        "statusCode": 200,
        "body": svg_content,
        "headers": {
            "Content-Type": "image/svg+xml"
        }
    }


def handler_seating(seating_input, conn):
    seating_id = seating_input["id"]
    input_path = f"{INPUT_PATH}/{seating_id}.json"
    output_path = f"{OUTPUT_PATH}/{seating_id}"

    print(f">> seating id: {seating_id}")
    print(f">> input path: {input_path}")
    print(f">> output path: {output_path}")

    # dump input to file
    with open(input_path, "w") as f:
        json.dump(seating_input, f)

    cmd = f"{HAMILTON_PATH} generate seating --input {input_path} --output {output_path}"

    # run exec_hamilton
    exec_hamilton(cmd)

    with open(f"{output_path}.svg", "r") as f:
        svg_content = f.read()
    ############################
    # get svg_seat_num from concerts table, only one value will be fetch
    cur = conn.cursor()
    cur.execute(f"SELECT svg_seat_num FROM concerts WHERE id = '{seating_id}'")
    svg_seat_num = cur.fetchone()[0]
    if svg_seat_num is not None:
        svg_seat_num = int(svg_seat_num)

    if svg_seat_num is not None and svg_seat_num >= seating_input["seats"]["purchased"]:
        print(
            f">> abort: avg_seat_num {svg_seat_num} is not None and  > purchased svg_seat_num {seating_input['seats']['purchased']}")
        return {
            "statusCode": 400,
            "body": "no need to update"
        }

    # update svg_seat_num in concerts table
    print(f">> update dase")
    cur = conn.cursor()
    cur.execute(f"UPDATE concerts SET svg_seat_num = '{seating_input['seats']['purchased']}' WHERE id = '{seating_id}'")
    # update svg_content to svg field in table concerts
    cur.execute(f"UPDATE concerts SET svg = '{svg_content}' WHERE id = '{seating_id}'")
    conn.commit()
    conn.close()

    return {
        "statusCode": 200,
        "body": svg_content,
        "headers": {
            "Content-Type": "image/svg+xml"
        }
    }


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
    print("original event:")
    print(event)
    print("\n\n")
    print("event['body']:")
    print("len(event['Records'])")
    print(len(event['Records']))
    print("\n\n")
    event = json.loads(event['Records'][0]['body'])
    print(event)
    # debug: return all the env para hostdb, hostname, etc
    # return {
    #     'statusCode': 200,
    #     'body': {
    #         'DB_HOST': DB_HOST,
    #         'DB_NAME': DB_NAME,
    #         'DB_PASS': DB_PASS,
    #         'DB_USERNAME': DB_USER,
    #     }
    # }

    # try:
    #     body = json.loads(event["body"])
    # except json.JSONDecodeError as e:
    #     return {
    #         'statusCode': 400,
    #         'body': json.dumps({"error": f"Invalid JSON: {str(e)}"}),
    #         'headers': {
    #             'Content-Type': 'application/json'
    #         }
    #     }
    # # body = event['body']
    #
    # event_name = body["event"]
    # _id = body["id"]
    event_name = event["event"]
    _id = event["id"]

    # if the event is not "concert" or "ticket", return 404
    if event_name != "concert" and event_name != "ticket":
        return {
            'statusCode': 404,
            'body': json.dumps('Something happened')
        }
    conn = connect_to_db()

    if event_name == "ticket":
        print(">> ticket event")
        ticket_info = get_ticket_info(_id, conn)
        handler_ticket(ticket_info, conn)
        conn.close()
        return {
            'statusCode': 200,
            'body': json.dumps(ticket_info)
        }
    elif event_name == "concert":
        print(">> concert event")
        concert_info = get_concert_info(_id, conn)
        # get svg_seat_num from concerts table, only one value will be fetch
        cur = conn.cursor()
        cur.execute(f"SELECT svg_seat_num FROM concerts WHERE id = '{_id}'")
        svg_seat_num = cur.fetchone()[0]
        # if svg_seat_num is none, keep it. else concert it to int
        if svg_seat_num is not None:
            svg_seat_num = int(svg_seat_num)
        # if the svg_seat_num is not None, generate pic
        if svg_seat_num is None:
            print(">> svg_seat_num is None, continue processing ")
            return handler_seating(concert_info, conn)
            # if the svg_Seat_num is greater than purchased_count, return 400
        if svg_seat_num >= concert_info["seats"]["purchased"]:
            print(f">> abort: svg_seat_num = {svg_seat_num} > purchased_count = {concert_info['seats']['purchased']}")
            return {
                'statusCode': 400,
                'body': json.dumps({"error": "Invalid seating"}),
                'headers': {
                    'Content-Type': 'application/json'
                }
            }

        return handler_seating(concert_info, conn)

    return {
        'statusCode': 404,
        'body': json.dumps({"error": f"Invalid UUID: {str(e)}"}),
        'headers': {
            'Content-Type': 'application/json'
        }
    }
