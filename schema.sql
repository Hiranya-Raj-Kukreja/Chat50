CREATE TABLE people (
    id INTEGER NOT NULL,
    username TEXT NOT NULL,
    hash TEXT NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE friends (
    id INTEGER NOT NULL,
    person_id INTEGER NOT NULL,
    friend_id INTEGER NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY(person_id) REFERENCES people(id),
    FOREIGN KEY(friend_id) REFERENCES people(id)
);

CREATE TABLE conversations (
    id INTEGER NOT NULL,
    sender_id INTEGER NOT NULL,
    receiver_id INTEGER NOT NULL,
    message TEXT NOT NULL,
    status TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(id),
    FOREIGN KEY(sender_id) REFERENCES people(id),
    FOREIGN KEY(receiver_id) REFERENCES people(id)
);

CREATE TABLE account (
    id INTEGER NOT NULL,
    person_id INTEGER NOT NULL,
    dp_src TEXT,
    PRIMARY KEY(id),
    FOREIGN KEY(person_id) REFERENCES people(id)
);

CREATE TABLE friend_request (
    sender_id INTEGER NOT NULL,
    receiver_id INTEGER NOT NULL,
    status TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(sender_id) REFERENCES people(id),
    FOREIGN KEY(receiver_id) REFERENCES people(id)
);
