-- reports.sql - the reports

\echo '--- All expenses ---'
SELECT e.id, e.expense_date, e.description, e.amount, c.name AS category
FROM expenses e
JOIN categories c ON c.id = e.category_id
ORDER BY e.expense_date, e.id;

\echo '--- Total per category ---'
SELECT c.name AS category, COUNT(*) AS no_of_expenses, SUM(e.amount) AS total
FROM expenses e
JOIN categories c ON c.id = e.category_id
GROUP BY c.name
ORDER BY total DESC;

\echo '--- Top 5 biggest expenses ---'
SELECT e.expense_date, e.description, e.amount, c.name AS category
FROM expenses e
JOIN categories c ON c.id = e.category_id
ORDER BY e.amount DESC
LIMIT 5;

\echo '--- Total spent ---'
SELECT COUNT(*) AS no_of_expenses, SUM(amount) AS total_spent
FROM expenses;
