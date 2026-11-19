# Expense Tracker (Python + PostgreSQL + Docker)

A command line project that reads an expense CSV file, **validates every row with Python (Pydantic)**,
saves the good rows in a **clean CSV**, and loads that file into a **PostgreSQL** database.
PostgreSQL and the Python app both run in **Docker**.

## The workflow (explain it in this order)

```
 expenses.csv  --->  Python app (Pydantic)  --->  clean_expenses.csv  --->  PostgreSQL  --->  SQL reports
  (raw data)         checks every row             only good rows           staging table        JOIN, GROUP BY,
                     prints rejected rows                                  -> real tables       SUM, COUNT ...
```

1. **Python app** (`app/main.py`) asks for a CSV path, reads the file line by line and splits each line by commas.
2. Each row goes into the **Pydantic model** (`app/models.py`). Pydantic checks the **data types**
   (real date, amount is a number). Wrong rows are rejected with the row number and the reason.
3. Our own `if` rules check the rest: description/category not empty, amount greater than 0.
4. Only valid rows are written to `data/clean_expenses.csv`.
5. **PostgreSQL** (`sql/load.sql`) copies the clean file into a `staging` table, then moves the data into
   `categories` and `expenses` (an expense stores the `category_id`).
6. `sql/reports.sql` shows the reports.

Python and PostgreSQL are kept separate on purpose: the **shared project folder** (Docker volume, `-v`) is the bridge.

## Project structure

```
expense-tracker/
├── app/
│   ├── main.py          # the CLI: read CSV, validate, write clean CSV
│   └── models.py        # Pydantic model (Expense)
├── sql/
│   ├── schema.sql       # creates the tables
│   ├── load.sql         # clean CSV -> staging -> categories + expenses
│   └── reports.sql      # the 4 reports
├── data/
│   ├── sample_expenses.csv        # 18 good rows
│   └── expenses_with_errors.csv   # 7 rows, 5 of them wrong on purpose
├── Dockerfile           # image for the Python app
├── .env                 # setting for the Python app (not pushed to GitHub)
├── .env.example         # copy of .env to show the format
└── .gitignore
```

## How to run

Run these in the VS Code terminal (PowerShell), inside the `expense-tracker` folder.

```
docker build -t expense-app .

docker run --name expense-db -e POSTGRES_USER=expense_user -e POSTGRES_PASSWORD=expense_pass -e POSTGRES_DB=expense_db -v "${PWD}:/project" -d postgres:16
```
(wait ~10 seconds)
```
docker exec expense-db psql -U expense_user -d expense_db -f /project/sql/schema.sql
docker run --rm -it -v "${PWD}:/project" expense-app          (type: ../data/sample_expenses.csv)
docker exec expense-db psql -U expense_user -d expense_db -f /project/sql/load.sql
docker exec expense-db psql -U expense_user -d expense_db -f /project/sql/reports.sql
```

Other terminals: replace `${PWD}` with `%cd%` (cmd) or `$(pwd)` (Linux/Mac).

To see the validation errors, run the app again and type `../data/expenses_with_errors.csv`.

To start again from zero: run `schema.sql` again (it deletes and recreates the tables).
Do not run `load.sql` twice on the same file, or the rows will be stored twice.

Stop everything:
```
docker stop expense-db
docker rm expense-db
```

## Docker commands explained

| Part | Meaning |
|---|---|
| `docker build -t expense-app .` | build an image from the Dockerfile in this folder and name it `expense-app` |
| `docker run` | create and start a container from an image |
| `--name expense-db` | give the container a name |
| `-e NAME=value` | set an environment variable inside the container (the DB user, password, name) |
| `-v "${PWD}:/project"` | share my project folder with the container; it appears as `/project` |
| `-d` | run in the background (detached) |
| `--rm` | delete the container when it stops |
| `-it` | allow typing into the container (needed for `input()`) |
| `docker exec expense-db ...` | run a command inside the running database container |

No `-p` is used because we only talk to the database through `docker exec`.
(`-p 5432:5432` is only needed to connect from outside, for example from pgAdmin.)

## Database design

- `categories (id, name)`
- `expenses (id, expense_date, description, amount, category_id -> categories.id)`
- `staging (expense_date, description, amount, category)` - temporary waiting room
- One category has many expenses (one-to-many), connected with a foreign key.

## Where each topic from the sheet is used

| Sheet topic | Used in |
|---|---|
| Git & GitHub, branching | feature branches + pull requests (`GIT_WORKFLOW.md`) |
| Basic Linux commands | `cd`, `ls`, `mkdir`, `cp`, `cat` to create and check the project |
| VS Code | editor used to write the project |
| SDLC | Plan -> Design (tables, files) -> Code -> Test (error CSV) -> Run (Docker) |
| Cloud intro | the containers run the same on a laptop or a cloud server |
| PostgreSQL, SQL, advanced SQL | `schema.sql`, `load.sql`, `reports.sql` (JOIN, GROUP BY, SUM, COUNT, ORDER BY, LIMIT) |
| Python concepts | functions, variables, lists, tuples, loops, `if`, files, `input()`, `try/except` |
| Pydantic | `models.py`: `BaseModel` with data types |
| venv | `python -m venv .venv` to run the app without Docker |
| dotenv | `main.py` reads `CLEAN_FILE` from `.env` |
| uv | installs the packages in the `Dockerfile` (and locally: `uv pip install pydantic python-dotenv`) |
| Docker | `Dockerfile` for the app, `docker run` for PostgreSQL and the app |

## Run the Python app without Docker (optional)

```
python -m venv .venv
.venv\Scripts\activate                      (Linux/Mac: source .venv/bin/activate)
uv pip install pydantic python-dotenv
cd app
python main.py
```
