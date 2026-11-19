# main.py - the command line app: reads a CSV, validates every row, writes a clean CSV
import os

from dotenv import load_dotenv
from pydantic import ValidationError

from models import Expense

load_dotenv()                          # reads the .env file
CLEAN_FILE = os.getenv("CLEAN_FILE")   # where the clean rows will be saved


def check_rules(expense):
    """Our own rules (Pydantic only checks the data types). Returns a list of problems."""
    problems = []
    if expense.description == "" or len(expense.description) > 100:
        problems.append("description must be 1 to 100 characters")
    if expense.category == "" or len(expense.category) > 50:
        problems.append("category must be 1 to 50 characters")
    if not expense.amount > 0:
        problems.append("amount must be greater than 0")
    if expense.amount >= 100000000:
        problems.append("amount is too large")
    return problems


def main():
    print("===== Expense Tracker: validate a CSV file =====")
    path = input("Enter CSV file path (example: ../data/sample_expenses.csv): ").strip()

    if not os.path.exists(path):
        print("File not found: " + path)
        return

    file = open(path)
    lines = file.readlines()
    file.close()

    if len(lines) == 0 or lines[0].strip() != "date,description,amount,category":
        print("The first line must be: date,description,amount,category")
        return

    valid_expenses = []
    rejected = []          # each item is (row_number, reason)
    row_number = 1

    for line in lines[1:]:
        row_number = row_number + 1
        line = line.strip()
        if line == "":
            continue

        parts = line.split(",")
        if len(parts) != 4:
            rejected.append((row_number, "expected 4 columns"))
            continue

        # step 1: Pydantic checks the data types
        try:
            expense = Expense(
                expense_date=parts[0].strip(),
                description=parts[1].strip(),
                amount=parts[2].strip(),
                category=parts[3].strip(),
            )
        except ValidationError as error:
            problems = []
            for item in error.errors():
                problems.append(item["loc"][0] + ": " + item["msg"])
            rejected.append((row_number, "; ".join(problems)))
            continue

        # step 2: our own rules
        problems = check_rules(expense)
        if len(problems) > 0:
            rejected.append((row_number, "; ".join(problems)))
        else:
            valid_expenses.append(expense)

    # show the result
    print()
    print("Rows read    : " + str(len(valid_expenses) + len(rejected)))
    print("Valid rows   : " + str(len(valid_expenses)))
    print("Rejected rows: " + str(len(rejected)))
    for row_number, reason in rejected:
        print("  Row " + str(row_number) + " rejected -> " + reason)

    # save only the valid rows in a new CSV file
    out = open(CLEAN_FILE, "w")
    out.write("expense_date,description,amount,category\n")
    for expense in valid_expenses:
        out.write(str(expense.expense_date) + "," + expense.description + ","
                  + str(expense.amount) + "," + expense.category + "\n")
    out.close()

    print()
    print("Clean file saved: " + CLEAN_FILE)
    print("Next step: load it into PostgreSQL (see README).")


main()
