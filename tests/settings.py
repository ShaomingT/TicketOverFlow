LOCAL_API_URLS = {
    "user": "http://localhost:8888/api/v1/users",
    "ticket": "http://localhost:9999/api/v1/tickets",
    "concert": "http://localhost:7777/api/v1/concerts"
}

CLOUD_BASE = "http://ticketoverflow-1000892056.us-east-1.elb.amazonaws.com/api/v1"
CLOUD_API_URLS = {
    "user": CLOUD_BASE + "/users",
    "ticket": CLOUD_BASE + "/tickets",
    "concert": CLOUD_BASE + "/concerts"
}

#### modify to test locally or on cloud
CURR_URLS = CLOUD_API_URLS
