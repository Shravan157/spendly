import pytest
from database.db import add_expense, get_spending_summary, get_category_breakdown

def test_add_expense(db_conn):
    # Create a user first
    from database.db import create_user
    user_id = create_user("Expense User", "expense@example.com", "hash")

    exp_id = add_expense(user_id, 100.0, "Food", "2026-09-27", "Dinner")
    assert exp_id is not None

def test_spending_summary(db_conn):
    from database.db import create_user
    user_id = create_user("Summary User", "summary@example.com", "hash")

    add_expense(user_id, 50.0, "Food", "2026-09-27", "Lunch")
    add_expense(user_id, 150.0, "Bills", "2026-09-27", "Internet")

    summary = get_spending_summary(user_id)
    assert summary["total_spent"] == 200.0
    assert summary["total_transactions"] == 2
    assert summary["top_category"] == "Bills"

def test_category_breakdown(db_conn):
    from database.db import create_user
    user_id = create_user("Breakdown User", "breakdown@example.com", "hash")

    add_expense(user_id, 100.0, "Food", "2026-09-27", "Lunch")
    add_expense(user_id, 100.0, "Transport", "2026-09-27", "Taxi")

    breakdown = get_category_breakdown(user_id)
    assert len(breakdown) == 2
    assert breakdown[0]["percentage"] == 50.0
