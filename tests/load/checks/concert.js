import _ from "https://cdn.jsdelivr.net/npm/lodash@4.17.11/lodash.min.js";
import { parseHTML } from "k6/html";

export const checkConcertList = {
    "Response code of 200 (healthy)": (r) => r.status === 200,
    "Response is JSON": (r) => r.headers["Content-Type"] === "application/json",
    "Response is an array": (r) => _.isArray(r.json()),
    "Every element is an object": (r) => _.every(r.json(), _.isObject),
    "Every element has an id": (r) => _.every(r.json(), (o) => _.has(o, 'id')),
    "Every element has a name": (r) => _.every(r.json(), (o) => _.has(o, 'name')),
    "Every element has a date": (r) => _.every(r.json(), (o) => _.has(o, 'date')),
    "Every element has a venue": (r) => _.every(r.json(), (o) => _.has(o, 'venue')),
    "Every element has a capacity": (r) => _.every(r.json(), (o) => _.has(o, 'capacity')),
    "Every element has a status": (r) => _.every(r.json(), (o) => _.has(o, 'status')),

    "Every capacity is a number": (r) => _.every(r.json(), (o) => _.isNumber(o.capacity)),
    "Every status is one of 'ACTIVE', 'CANCELLED', or 'SOLD_OUT'" : (r) => _.every(r.json(), (o) => _.includes(['ACTIVE', 'CANCELLED', 'SOLD_OUT'], o.status)),
    "Every date is YYYY-MM-DD": (r) => _.every(r.json(), (o) => _.isMatch(o.date, /\d{4}-\d{2}-\d{2}/)),
};

export const checkConcert = {
    "Response code of 200 or 201 (healthy)": (r) => r.status === 200 || r.status === 201,
    "Response is an object": (r) => _.isObject(r.json()),
    "Response has an id": (r) => _.has(r.json(), 'id'),
    "Response has a name": (r) => _.has(r.json(), 'name'),
    "Response has a date": (r) => _.has(r.json(), 'date'),
    "Response has a venue": (r) => _.has(r.json(), 'venue'),
    "Response has a capacity": (r) => _.has(r.json(), 'capacity'),
    "Response has a status": (r) => _.has(r.json(), 'status'),

    "Capacity is a number": (r) => _.isNumber(r.json().capacity),
    "Status is one of 'ACTIVE', 'CANCELLED', or 'SOLD_OUT'" : (r) => _.includes(['ACTIVE', 'CANCELLED', 'SOLD_OUT'], r.json().status),
    "Date is YYYY-MM-DD": (r) => _.isMatch(r.json().date, /\d{4}-\d{2}-\d{2}/),
};

export const checkSeatingPlan = {
    "Response code of 200 (healthy)": (r) => r.status === 200,
    "Response is a SVG": (r) => r.headers["Content-Type"] === "image/svg+xml",
    "Response is a valid SVG": (r) => {
        const doc = parseHTML(r.body);
        return doc !== null;
    },
    /*"Response has a <desc> element": (r) => {
        const doc = parseHTML(r.body);
        return doc.find("desc").length > 0;
    },*/
    "<desc> has a value with three pipe-separated parts": (r) => {
        const doc = parseHTML(r.body);
        const desc = doc.find("desc").text();
        const parts = desc.split("|");
        return parts.length === 3;
    },
};
