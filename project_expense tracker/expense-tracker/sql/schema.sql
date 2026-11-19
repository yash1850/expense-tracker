-- schema.sql - creates the tables (safe to run again: it deletes and recreates them)

DROP TABLE IF EXISTS expenses;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS staging;

-- one category can have many expenses
CREATE TABLE categories (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE expenses (
    id           SERIAL PRIMARY KEY,
    expense_date DATE NOT NULL,
    description  VARCHAR(100) NOT NULL,
    amount       NUMERIC(10, 2) NOT NULL,
    category_id  INTEGER NOT NULL REFERENCES categories(id)
);

-- staging = a waiting room: the clean CSV is copied here first, exactly as it is
CREATE TABLE staging (
    expense_date DATE,
    description  VARCHAR(100),
    amount       NUMERIC(10, 2),
    category     VARCHAR(50)
);
