import _ from "https://cdn.jsdelivr.net/npm/lodash@4.17.11/lodash.min.js";

export const checkTicketList = {
    "Response code of 200 (healthy)": (r) => r.status === 200,
    "Response is JSON": (r) => r.headers["Content-Type"].includes("application/json"),
    "Response is an array": (r) => _.isArray(r.json()),
    "Every element has an id": (r) => _.every(r.json(), (e) => _.has(e, "id")),
    
    "Every element has a concert": (r) => _.every(r.json(), (e) => _.has(e, "concert")),
    "Every concert is an object": (r) => _.every(r.json(), (e) => _.isObject(e.concert)),
    "Every concert has an id": (r) => _.every(r.json(), (e) => _.has(e.concert, "id")),
    "Every concert has a url": (r) => _.every(r.json(), (e) => _.has(e.concert, "url")),
    "Every URL ends with the concert id": (r) => _.every(r.json(), (e) => e.concert.url.endsWith(e.concert.id)),
    
    "Every element has a user": (r) => _.every(r.json(), (e) => _.has(e, "user")),
    "Every user is an object": (r) => _.every(r.json(), (e) => _.isObject(e.user)),
    "Every user has an id": (r) => _.every(r.json(), (e) => _.has(e.user, "id")),
    "Every user has a url": (r) => _.every(r.json(), (e) => _.has(e.user, "url")),
    "Every URL ends with the user id": (r) => _.every(r.json(), (e) => e.user.url.endsWith(e.user.id)),
    
    "Every element has a print_status": (r) => _.every(r.json(), (e) => _.has(e, "print_status")),
    "Every print_status is one of NOT_PRINTED, PRINTED, ERROR, or PENDING": (r) => _.every(r.json(), (e) => ["NOT_PRINTED", "PRINTED", "ERROR", "PENDING"].includes(e.print_status)),
};

export const checkTicket = {
    "Response code of 200 or 201 (healthy)": (r) => r.status === 200 || r.status === 201,
    "Response is JSON": (r) => r.headers["Content-Type"].includes("application/json"),
    "Response is an object": (r) => _.isObject(r.json()),
    "Response has an id": (r) => _.has(r.json(), "id"),
    
    "Response has a concert": (r) => _.has(r.json(), "concert"),
    "Concert is an object": (r) => _.isObject(r.json().concert),
    "Concert has an id": (r) => _.has(r.json().concert, "id"),
    "Concert has a url": (r) => _.has(r.json().concert, "url"),
    "URL ends with the concert id": (r) => r.json().concert.url.endsWith(r.json().concert.id),

    "Response has a user": (r) => _.has(r.json(), "user"),
    "User is an object": (r) => _.isObject(r.json().user),
    "User has an id": (r) => _.has(r.json().user, "id"),
    "User has a url": (r) => _.has(r.json().user, "url"),
    "URL ends with the user id": (r) => r.json().user.url.endsWith(r.json().user.id),

    "Response has a print_status": (r) => _.has(r.json(), "print_status"),
    "Print_status is one of NOT_PRINTED, PRINTED, ERROR, or PENDING": (r) => ["NOT_PRINTED", "PRINTED", "ERROR", "PENDING"].includes(r.json().print_status),
};

export const checkPrintedTicket = {
    "Response code of 200 (healthy)": (r) => r.status === 200,
    "Response is a SVG": (r) => r.headers["Content-Type"].includes("image/svg+xml"),
    "Response is valid SVG": (r) => {
        const parser = new DOMParser();
        const doc = parser.parseFromString(r.text(), "image/svg+xml");
        return doc.documentElement.nodeName === "svg";
    },
    "SVG has a <desc> element": (r) => {
        const parser = new DOMParser();
        const doc = parser.parseFromString(r.text(), "image/svg+xml");
        return doc.querySelector("desc") !== null;
    }
};

