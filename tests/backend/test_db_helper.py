from backend import db_helper
import pytest

def test_fetch_expense_for_date():
    expenses = db_helper.fetch_expense_for_date('2024-08-15')
    assert len(expenses) == 1
    assert expenses[0]['amount'] == 10

def test_fetch_expenses_for_date_invalid_date() :
    expenses = db_helper. fetch_expense_for_date("9999-08-15")
    assert len (expenses) == 0

def test_fetch_expense_summary_invalid_range():
    summary = db_helper. fetch_expense_summary ("2099-01-01", "2099-12-03")
    assert len (summary) == 0