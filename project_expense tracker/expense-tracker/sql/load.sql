-- load.sql - moves the clean CSV into the real tables

-- 1. copy the CSV file into the waiting room
COPY staging FROM '/project/data/clean_expenses.csv' WITH (FORMAT csv, HEADER true);

-- 2. add the new categories (each name only once)
INSERT INTO categories (name)
SELECT DISTINCT category
FROM staging
WHERE category NOT IN (SELECT name FROM categories);

-- 3. add the expenses, replacing the category name with its id
INSERT INTO expenses (expense_date, description, amount, category_id)
SELECT s.expense_date, s.description, s.amount, c.id
FROM staging s
JOIN categories c ON c.name = s.category;

-- 4. empty the waiting room
DELETE FROM staging;
