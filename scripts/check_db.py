"""Check database connection and tables."""
from backend.app.db import engine
from sqlalchemy import inspect

try:
    # Test connection
    with engine.connect() as conn:
        print("Successfully connected to database!")
        print(f"Database URL: {engine.url}")

    # Check tables
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    print(f"\nTables in database:")
    if tables:
        for table in tables:
            print(f"  - {table}")
    else:
        print("  (no tables found)")

except Exception as e:
    print(f"Error: {e}")
