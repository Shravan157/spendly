import pytest
from database.db import create_user, get_user_by_email, get_user_by_id

def test_create_user(db_conn):
    user_id = create_user("Test User", "test@example.com", "hashed_password")
    assert user_id is not None

    user = get_user_by_email("test@example.com")
    assert user is not None
    assert user["name"] == "Test User"

def test_create_user_duplicate_email(db_conn):
    create_user("User 1", "duplicate@example.com", "hash1")
    import sqlite3
    with pytest.raises(sqlite3.IntegrityError):
        create_user("User 2", "duplicate@example.com", "hash2")

def test_get_user_by_id(db_conn):
    user_id = create_user("ID User", "id@example.com", "hash")
    user = get_user_by_id(user_id)
    assert user is not None
    assert user["email"] == "id@example.com"
