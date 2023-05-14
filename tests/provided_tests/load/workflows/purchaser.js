import http from "k6/http";
import { check, sleep } from "k6";
import { Rate, Counter } from "k6/metrics";

import { checkUser, checkIsUser } from "../checks/user.js";
import { checkTicket } from "../checks/ticket.js";

const BASE_URL = __ENV.TEST_HOST;

const errors = new Counter("errors");
const tickets = new Counter("tickets");


export function purchaser(data) {
    // Login and get my user id
    const userId = "00000000-0000-0000-0000-000000002357";
    let res = http.get(`${BASE_URL}/users/${userId}`);
    try {
        check(res, checkIsUser("${userId}", "Virginia Moen", "labadie@example.org"), { endpoint : "/users" });
    } catch (e) {
        console.log(e);
        errors.add(1, { endpoint : "/users" });
    }

    // Purchase a ticket
    let url = BASE_URL + `/tickets`;
    let payload = JSON.stringify({
        concert_id: data.concertId,
        user_id: userId
    });
    res = http.post(url, payload, {headers: {"Content-Type": "application/json"}});
    try {
        let success = check(res, checkTicket, { endpoint : "/tickets" });
        if (success) {
            tickets.add(1, { endpoint : "/tickets" });
        }
    } catch (e) {
        console.log(e);
        errors.add(1, { endpoint : "/tickets" });
    }

    // View my ticket
    url = BASE_URL + `/tickets/${res.json("id")}`;
    res = http.get(url);
    try {
        check(res, checkTicket, { endpoint : "/tickets" });
    } catch (e) {
        console.log(e);
        errors.add(1, { endpoint : "/tickets" });
    }
}
