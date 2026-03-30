-- database my_db
CREATE TABLE users (
    user_id INT PRIMARY KEY,
	role_id SMALLINT NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    second_name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20) UNIQUE,
    active_flag BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE roles(
role_id SMALLINT PRIMARY KEY,
role_name VARCHAR(20) UNIQUE,
description TEXT
);