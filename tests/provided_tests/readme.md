## Conformance
docker pull ghcr.io/csse6400/ticketoverflow-conformance:latest
docker run --net='host' -e TEST_HOST='http://ticketoverflow-1020805617.us-east-1.elb.amazonaws.com/api/v1' ghcr.io/csse6400/ticketoverflow-conformance:latest

## Scalability
docker pull ghcr.io/csse6400/ticketoverflow-load:latest
docker run --net='host' -e TEST_HOST='http://localhost:6400/api/v1' ghcr.io/csse6400/ticketoverflow-load:latest


http://ticketoverflow-1020805617.us-east-1.elb.amazonaws.com/api/v1