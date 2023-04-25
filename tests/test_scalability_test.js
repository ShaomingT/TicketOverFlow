import http from 'k6/http';
import {sleep, check} from 'k6';

export const options = {
    stages: [
        {target: 10, duration: '10s'},
        // {target: 300, duration: '10s'},
        // {target: 400, duration: '10s'},
        // {target: 400, duration: '10s'},
        // {target: 2400, duration: '60s'},
        // {target: 4000, duration: '10s'},
        // {target: 2400, duration: '60s'},
        // {target: 2400, duration: '60s'},
        // {target: 2400, duration: '60s'},
        // {target: 2400, duration: '60s'},

    ],
};

export default function () {
    const res = http.get("http://ticketoverflow-2138364935.us-east-1.elb.amazonaws.com/api/v1/tickets/health");
    check(res, {'status was 200': (r) => r.status == 200});
    sleep(1);
}