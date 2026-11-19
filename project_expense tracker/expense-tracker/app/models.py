# models.py - the Pydantic model: describes ONE expense row and its data types
from datetime import date

from pydantic import BaseModel


class Expense(BaseModel):
    expense_date: date     # Pydantic checks this is a real date, e.g. 2026-09-01
    description: str       # must be text
    amount: float          # Pydantic checks this is a number
    category: str          # must be text
