import http from "k6/http";
import { check, sleep } from "k6";
import { Rate, Counter } from "k6/metrics";

const BASE_URL = __ENV.TEST_HOST;

const errors = new Counter("errors");

import { purchaser } from "./workflows/purchaser.js";

export const options = {
    scenarios: {
        purchaser: {
            executor: "ramping-vus",
            stages: [
                { duration: "6m", target: 250 },
                { duration: "3m", target: 125 },
                { duration: "2m", target: 0 },
            ],
            exec: 'generalPurchaser',
        },
    },
    tags: {
        scenario: "general",
    },
    minIterationDuration: '10s'
};

export function setup() {
    // Create a concert
    const res = http.post(`${BASE_URL}/concerts`, JSON.stringify({
        name: "Hamilton",
        venue: "Lyric Theatre at QPAC",
        date: "2023-08-05",
        capacity: 3000,
        status: "ACTIVE"
    }), {
        headers: {"Content-Type": "application/json"},
    });
        
    return { concertId: res.json("id") };
}

export const MAX_ITERATIONS = 2900;

export function generalPurchaser(data) {
    if (__ITER >= MAX_ITERATIONS) {
        return;
    }

    purchaser(data);
    sleep(10);
}
