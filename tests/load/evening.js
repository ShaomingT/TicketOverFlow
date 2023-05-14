import http from "k6/http";
import { check, sleep } from "k6";
import { Rate, Counter } from "k6/metrics";
import { randomIntBetween } from 'https://jslib.k6.io/k6-utils/1.2.0/index.js';


import { checkSeatingPlan } from "./checks/concert.js";

const BASE_URL = __ENV.TEST_HOST;

const errors = new Counter("errors");

import { purchaser } from "./workflows/purchaser.js";
import { staff } from "./workflows/staff.js";

export const options = {
    scenarios: {
        concert1Purchaser: {
            executor: "ramping-vus",
            stages: [
                { duration: "6m", target: 120 },
                { duration: "2m", target: 60 },
                { duration: "2m", target: 0 },
            ],
            exec: 'concert1Purchaser',
        },
        concert2Purchaser: {
            executor: "ramping-vus",
            stages: [
                { duration: "2m", target: 60 },
                { duration: "2m", target: 180 },
                { duration: "2m", target: 0 },
            ],
            exec: 'concert2Purchaser',
        },
        concert3Purchaser: {
            executor: "ramping-vus",
            stages: [
                { duration: "2m", target: 10 },
                { duration: "4m", target: 80 },
                { duration: "1m", target: 0 },
            ],
            exec: 'concert3Purchaser',
        },
        staff: {
            executor: "shared-iterations",
            vus: 5,
            iterations: 50,
            maxDuration: "6m",
            exec: 'eveningStaff',
        },
    },
    tags: {
        scenario: "evening",
    },
    minIterationDuration: '10s'
};

export function setup() {
    // Create a concert
    const concert1 = http.post(`${BASE_URL}/concerts`, JSON.stringify({
        name: "Phantom of the Opera",
        venue: "Lyric Theatre at QPAC",
        date: "2023-06-05",
        capacity: 3000,
        status: "ACTIVE"
    }), {
        headers: {"Content-Type": "application/json"},
    });
    const concert2 = http.post(`${BASE_URL}/concerts`, JSON.stringify({
        name: "The Lion King",
        venue: "Sydney Lyric Theatre",
        date: "2023-06-27",
        capacity: 2000,
        status: "ACTIVE"
    }), {
        headers: {"Content-Type": "application/json"},
    });
    const concert3 = http.post(`${BASE_URL}/concerts`, JSON.stringify({
        name: "The Book of Mormon",
        venue: "Princess Theatre",
        date: "2023-07-01",
        capacity: 1500,
        status: "ACTIVE"
    }), {
        headers: {"Content-Type": "application/json"},
    });

        
    return { concert1Id: concert1.json("id"), concert2Id: concert2.json("id"), concert3Id: concert3.json("id") };
}

export function concert1Purchaser(data) {
    if (__ITER >= 2800) {
        return;
    }

    purchaser({ concertId: data.concert1Id });
    sleep(10);
}

export function concert2Purchaser(data) {
    if (__ITER >= 1800) {
        return;
    }

    purchaser({ concertId: data.concert2Id });
    sleep(10);
}

export function concert3Purchaser(data) {
    if (__ITER >= 1300) {
        return;
    }

    purchaser({ concertId: data.concert3Id });
    sleep(10);
}

export function eveningStaff(data) {
    let concert = randomIntBetween(1, 3);
    staff({ concertId: data[`concert${concert}Id`] });
    sleep(10);
}

