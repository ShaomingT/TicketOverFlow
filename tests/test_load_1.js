import http from 'k6/http';
import { sleep, check } from 'k6';

const config = {
  requestsPerSecond: 100, // Number of requests per second
  testDuration: '5m', // Test duration
};

export let options = {
  vus: config.requestsPerSecond,
  duration: config.testDuration,
};

export default function () {
  const url = 'http://ticketoverflow-1042601666.us-east-1.elb.amazonaws.com/api/v1/tickets/health';

  let response = http.get(url);

  check(response, {
    'status is 200': (r) => r.status === 200,
  });

  // Sleep to achieve the desired request rate.
  sleep(1 / (config.requestsPerSecond / options.vus));
}
