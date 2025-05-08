CREATE TABLE clan (
    id SERIAL PRIMARY KEY,
    tag TEXT NOT NULL,
    name TEXT NOT NULL
);

CREATE TABLE user_detailed_info (
    id SERIAL PRIMARY KEY,
    crowns INTEGER NOT NULL,
    max_crowns INTEGER NOT NULL,
    clan_id INTEGER REFERENCES clan(id),
    updated_ts TIMESTAMP
);

CREATE TABLE battle_type (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    name VARCHAR(100),
    tag TEXT NOT NULL,
    is_super_user BOOLEAN NOT NULL DEFAULT FALSE,
    user_detailed_info_id INTEGER REFERENCES user_detailed_info(id)
);

CREATE TABLE subscribe (
    id SERIAL PRIMARY KEY,
    user_id1 INTEGER REFERENCES "user"(id) NOT NULL,
    user_id2 INTEGER REFERENCES "user"(id) NOT NULL,
    battle_type_id INTEGER REFERENCES battle_type(id) NOT NULL
);

CREATE TABLE battle_record (
    id SERIAL PRIMARY KEY,
    subscribe_id INTEGER REFERENCES subscribe(id) ON DELETE CASCADE NOT NULL,
    user1_score INTEGER NOT NULL,
    user2_score INTEGER NOT NULL,
    user1_get_crowns INTEGER NOT NULL,
    user2_get_crowns INTEGER NOT NULL,
    user1_card_ids INTEGER[] NOT NULL,
    user2_card_ids INTEGER[] NOT NULL,
    replay TEXT,
    time TIMESTAMP NOT NULL,
    winner_id INTEGER REFERENCES "user"(id) NOT NULL
);

CREATE TABLE card (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    level INTEGER NOT NULL
);

INSERT INTO clan (tag, name)
VALUES ('tag-1', 'Кафедра 910'),
       ('tag-2', 'Кафедра 911'),
       ('tag-3', 'Кафедра 912');

INSERT INTO user_detailed_info (crowns, max_crowns, clan_id, updated_ts)
VALUES (1234, 5678, 1, NULL),
       (1234, 5678, 2, NULL),
       (1234, 5678, 3, NULL),
       (1234, 5678, 1, NULL);

INSERT INTO "user" (email, password, name, tag, is_super_user, user_detailed_info_id)
VALUES ('user1@example.com', '$2b$12$EK0Ww/5JDZHe.k6BwTEbDOWSCvgEehXwOOD9xp0U5b8H67nu19N5C', 'user One', 'VGJ80GUR', TRUE, 1),
       ('user2@example.com', '$2b$12$EK0Ww/5JDZHe.k6BwTEbDOWSCvgEehXwOOD9xp0U5b8H67nu19N5C', 'user Two', 'RV99LRYP', FALSE, 2),
       ('user3@example.com', '$2b$12$EK0Ww/5JDZHe.k6BwTEbDOWSCvgEehXwOOD9xp0U5b8H67nu19N5C', 'user Three', 'PRV9RPRL2', FALSE, 3),
       ('user4@example.com', '$2b$12$EK0Ww/5JDZHe.k6BwTEbDOWSCvgEehXwOOD9xp0U5b8H67nu19N5C', 'user Four', '2UOGPV9PQ', FALSE, 4);

INSERT INTO battle_type (name)
VALUES ('Rating'),
       ('Default');

INSERT INTO subscribe (user_id1, user_id2, battle_type_id)
VALUES (1, 2, 1),
       (1, 3, 1),
       (2, 3, 1),
       (3, 4, 1);

INSERT INTO battle_record (subscribe_id, user1_score, user2_score, user1_get_crowns, user2_get_crowns, user1_card_ids, user2_card_ids, replay, time, winner_id)
VALUES (1, 10, 5, 2, 1, '{1,2,3}', '{4,1,2}', NULL, CURRENT_TIMESTAMP, 1),
       (2, 8, 12, 1, 3, '{1,2,3}', '{4,1,2}', NULL, CURRENT_TIMESTAMP, 2),
       (3, 15, 10, 3, 2, '{1,2,3}', '{4,1,2}', NULL, CURRENT_TIMESTAMP, 1),
       (4, 20, 18, 4, 3, '{1,2,3}', '{4,1,2}', NULL, CURRENT_TIMESTAMP, 3);

INSERT INTO card (name, type, level)
VALUES ('Golem', 'Type A', 1),
       ('Princess', 'Type B', 2),
       ('Miner', 'Type A', 3),
       ('Larry', 'Type B', 4);


CREATE OR REPLACE FUNCTION update_updated_ts()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_ts = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_user_detailed_info_updated_ts
BEFORE UPDATE ON user_detailed_info
FOR EACH ROW
EXECUTE FUNCTION update_updated_ts();