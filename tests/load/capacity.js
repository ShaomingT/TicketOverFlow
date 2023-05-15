import http from "k6/http";
import { sleep } from "k6";

export let options = {
  vus: 200,
  duration: "1m"
};

const ENDPOINT = 'http://ticketoverflow-1711289896.us-east-1.elb.amazonaws.com/api/v1/tickets/health';

export default function() {
  http.get(`${ENDPOINT}`);
  sleep(1); // Each VU will sleep for 1 second between requests, which means we'll have 50 requests per second in total
}
