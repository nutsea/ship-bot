CREATE TABLE yuan (
    id SERIAL PRIMARY KEY,
    course DECIMAL
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    track VARCHAR(255),
    status INT
);