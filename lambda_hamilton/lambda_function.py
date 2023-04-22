import json
import subprocess
import os

# context ticket format
# context =
# {"event": "ticket",
#            "content": {
#         "id": "12345678-1234-1234-1234-123456789012",
#         "name": "Evan Hughes",
#         "email": "example@uq.edu.au",
#         "concert": {
#             "id": "12345678-1234-1234-1234-123456789012",
#             "name": "Phantom of the Opera",
#             "date": "2023-06-07",
#             "venue": "Sydney Opera House"
#         }
# }

# context seating format
# context =
# {"event": "seating",
#            "content": {
#   "id": "12345678-1234-1234-1234-123456789012",
#   "name": "Phantom of the Opera",
#   "date": "2023-06-07",
#   "venue": "Sydney Opera House",
#   "seats": {
#     "max": 5738,
#     "purchased": 2340
#   }
# }

INPUT_PATH = "/tmp"
OUTPUT_PATH = "/tmp"
HAMILTON_PATH = "./bin/hamilton-v1.1.0-linux-amd64"


def exec_hamilton(cmd):
    print(">> start exec hamilton")
    try:
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
        print(">> Output:", output.decode('utf-8'))
    except subprocess.CalledProcessError as e:
        print(">> Error output:", e.output.decode('utf-8'))
        raise e

    print(">> hamilton finished")


def handler_ticket(ticket_input):
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

    return {
        "statusCode": 200,
        "body": svg_content,
        "headers": {
            "Content-Type": "image/svg+xml"
        }
    }


def handler_seating(seating_input):
    seating_id = seating_input["id"]
    input_path = f"{INPUT_PATH}/{seating_id}.json"
    output_path = f"{OUTPUT_PATH}/{seating_id}"

    print(f">> seating id: {seating_id}")
    print(f">> input path: {input_path}")
    print(f">> output path: {output_path}")

    # dump input to file
    with open(input_path, "w") as f:
        json.dump(seating_input, f)

    # list files in /tmp
    print(">> list files in /tmp")
    for file in os.listdir("/tmp"):
        print(file)

    cmd = f"{HAMILTON_PATH} generate seating --input {input_path} --output {output_path}"

    # run exec_hamilton
    exec_hamilton(cmd)

    with open(f"{output_path}.svg", "r") as f:
        svg_content = f.read()

    return {
        "statusCode": 200,
        "body": svg_content,
        "headers": {
            "Content-Type": "image/svg+xml"
        }
    }


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
    event_input = body["content"]

    if event_name == "ticket":
        print(">> Event: Ticket")
        return handler_ticket(event_input)
    elif event_name == "seating":
        print(">> Event: Seating")
        return handler_seating(event_input)
    else:
        return{
            "statusCode": 400,
        }

