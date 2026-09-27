import pytest
from app import app as flask_app
import os
import sqlite3

@pytest.fixture
def app():
    # Use a shared in-memory database so all connections see the same tables
    os.environ['DATABASE_PATH'] = 'file:memdb1?mode=memory&cache=shared'

    flask_app.config.update({
        "TESTING": True,
        "SECRET_KEY": "test-secret-key",
    })

    # Force a reload of the DB path in the module
    import database.db
    import importlib
    importlib.reload(database.db)

    # Initialize the DB
    with flask_app.app_context():
        from database.db import init_db
        init_db()

    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def db_conn(app):
    from database.db import get_db
    with app.app_context():
        return get_db()
