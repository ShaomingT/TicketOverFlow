import _ from "https://cdn.jsdelivr.net/npm/lodash@4.17.11/lodash.min.js";

export const checkUserList = {
    "Response code of 200 (healthy)": (r) => r.status === 200,
    "Response is JSON": (r) => r.headers["Content-Type"].includes("application/json"),
    "Response is an array": (r) => _.isArray(r.json()),
    "Every element is an object": (r) => _.every(r.json(), _.isObject),

    "Every element has an id": (r) => _.every(r.json(), (e) => _.has(e, "id")),
    "Every element has a name": (r) => _.every(r.json(), (e) => _.has(e, "name")),
    "Every element has an email": (r) => _.every(r.json(), (e) => _.has(e, "email")),
};

export const checkUser = {
    "Response code of 200 (healthy)": (r) => r.status === 200,
    "Response is JSON": (r) => r.headers["Content-Type"].includes("application/json"),
    "Response is an object": (r) => _.isObject(r.json()),
    "Response has an id": (r) => _.has(r.json(), "id"),
    "Response has a name": (r) => _.has(r.json(), "name"),
    "Response has an email": (r) => _.has(r.json(), "email"),
};

export const checkIsUser = (id, name, email) => ({
    "Response code of 200 (healthy)": (r) => r.status === 200,
    "Response is JSON": (r) => r.headers["Content-Type"].includes("application/json"),
    "Response is an object": (r) => _.isObject(r.json()),
    "Response has an id": (r) => _.has(r.json(), "id"),
    "Response has a name": (r) => _.has(r.json(), "name"),
    "Response has an email": (r) => _.has(r.json(), "email"),
    //"Response id is correct": (r) => r.json().id === id,
    "Response name is correct": (r) => r.json().name === name,
    "Response email is correct": (r) => r.json().email === email,
});

