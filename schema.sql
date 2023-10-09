DROP TABLE IF EXISTS user;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fullname TEXT NOT NULL,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    pass TEXT NOT NULL,
    gender TEXT NOT NULL
);

DROP TABLE IF EXISTS TODO;

CREATE TABLE TODO (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    todo TEXT NOT NULL
);