# TicketOverFlow
A scalable online ticketing booking platform with a microservice architecture.

# Features
Endpoints List
- Concert Service
  - GET /concert/health
  - GET /concerts - List all the concerts registered with TicketOverFlow
  - POST /concerts - Register a new concert for TicketOverFlow
  - GET /concerts/{id} - Get details for a particular concert.
  - PUT /concerts/{id} - Update details about a concert
  - GET /concerts/{id}/seats - Get the seating plan as an SVG for a particular concert.
- Ticket Service
  - GET /tickets/health
  - GET /tickets - List all the purchased tickets
  - POST /tickets - Purchase a ticket for a concert
  - GET /tickets/{id} - Get information for a particular ticket
  - POST /tickets/{id}/print - Request that a ticket be printed asynchronously.
  - GET /tickets/{id}/print - Get the printed ticket if it exists.
- User Service
  - GET /users/health
  - GET /users - List all registered users for the service.
  - GET /users/{id} Get information for a particular user.

## Dependencies

Before deploying,the following dependencies must be installed:

- Python 3.10 - Execute script to init USER table
- Terraform 1.4.6
- zip - Used to zip the lambda function
- Psycopg2 2.9.1 - Used to connect to RDS in Python
- pipenv
- Docker - Used to build docker image by Terraform
- registry.terraform.io/kreuzwerker/docker - Used to push docker image to ECR

Install dependencies by apt

```angular2html
echo "installing dependencies..."
apt update -y
apt install python3 -y
apt install python3-pip -y
python3 -m pip install psycopg2-binary

```

## Deployment

1. Fill `credentials` file.
2. Run `./deoply.sh` to deploy the infrastructure.
