CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    password TEXT
);

CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    user_id1 INTEGER REFERENCES users,
    user_id2 INTEGER REFERENCES users
);

CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    group_name TEXT
);

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conv_id INTEGER REFERENCES conversations,
    group_id INTEGER REFERENCES groups,
    message TEXT
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