CREATE SCHEMA Auth_DB;
SELECT SCHEMA 'Auth_DB';

CREATE TABLE AuthTable (
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    PRIMARY KEY (username, password)
);

INSERT INTO AuthTable (username, password) VALUES
('Vic', '123'),
('Del', '345'),
('Ale', '567'),
('Vas', '789');