CREATE DATABASE ticketoverflow;
\c ticketoverflow

CREATE TABLE users (
  id UUID PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL
);

CREATE TABLE tickets (
  id UUID PRIMARY KEY,
  concert_id UUID NOT NULL,
  user_id UUID NOT NULL,
  print_status VARCHAR(255),
  svg TEXT
);

CREATE TABLE concerts (
  id UUID PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  venue VARCHAR(255) NOT NULL,
  date VARCHAR(255) NOT NULL,
  capacity INTEGER NOT NULL,
  status VARCHAR(255),
  svg TEXT,
  svg_seat_num INTEGER
);
