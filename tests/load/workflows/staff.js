import http from "k6/http";
import { check, sleep } from "k6";
import { Rate, Counter } from "k6/metrics";

import { checkSeatingPlan } from "../checks/concert.js";

const BASE_URL = __ENV.TEST_HOST;

const errors = new Counter("errors");
const seatings = new Counter("seatings");
const attempted = new Counter("attempted_seatings");

export function staff(data) {
    attempted.add(1);

    const concertId = data.concertId;

    // Request a seating plan - allow 3 minutes for a successful response
    let timeout = 180;
    while (timeout > 0) {
        const res = http.get(`${BASE_URL}/concerts/${concertId}/seats`);
        try {
            let success = check(res, checkSeatingPlan, { "endpoint": "/concerts/{id}/seats", "allowErrors": true });
            if (success) {
                console.log(`Seating plan for concert ${concertId} retrieved successfully`);
                break;
            }
        } catch (error) {
        }
        timeout -= 10;
        sleep(10);
    }

    const staffRes = http.get(`${BASE_URL}/concerts/${concertId}/seats`);
    try {
        let success = check(staffRes, checkSeatingPlan, { "endpoint": "/concerts/{id}/seats" });
        if (success) {
            seatings.add(1, { "endpoint": "/concerts/{id}/seats" });
        }
    } catch (e) {
        console.error(e);
        errors.add(1, { "endpoint": "/concerts/{id}/seats" });
    }
}

