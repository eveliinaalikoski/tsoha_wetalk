CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    password TEXT
);

CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    user_id1 INTEGER REFERENCES users,
    user_id2 INTEGER REFERENCES users
);

CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    group_name TEXT UNIQUE
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    conv_id INTEGER REFERENCES conversations,
    group_id INTEGER REFERENCES groups,
    message TEXT,
    sent_at TIMESTAMP
);

CREATE TABLE users_groups (
    id SERIAL PRIMARY KEY,
    group_id INTEGER REFERENCES groups,
    user_id INTEGER REFERENCES users
);

CREATE TABLE admins (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    group_id INTEGER REFERENCES groups
);