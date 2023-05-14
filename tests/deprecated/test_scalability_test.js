import http from 'k6/http';
import {sleep, check} from 'k6';

export const options = {
    stages: [
        {target: 200, duration: '10s'},
    ],
};

export default function () {
    const res = http.get("http://ticketoverflow-1042601666.us-east-1.elb.amazonaws.com/api/v1/tickets/health");
    check(res, {'status was 200': (r) => r.status == 200});
    sleep(5);
}