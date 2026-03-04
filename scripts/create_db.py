"""
Create the application database if it does not exist.
Uses the same DATABASE_URL from config (.env); connects to 'postgres' to create the target db.

Run from project root:  poetry run python scripts/create_db.py
"""
import os
import sys
from urllib.parse import urlparse, urlunparse

# Ensure project root is on path so "app" can be imported
_script_dir = os.path.dirname(os.path.abspath(__file__))
_root = os.path.dirname(_script_dir)
if _root not in sys.path:
    sys.path.insert(0, _root)

def main():
    try:
        from app.core.config import settings
    except Exception as e:
        print("Could not load config:", e, file=sys.stderr)
        sys.exit(1)

    url = urlparse(settings.DATABASE_URL)
    db_name = url.path.lstrip("/") or "eventdb"
    # Connect to default 'postgres' database to create our db
    postgres_url = urlunparse((url.scheme, url.netloc, "/postgres", url.params, url.query, url.fragment))

    try:
        import psycopg2
        from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
    except ImportError:
        print("psycopg2 is required. Install with: poetry install", file=sys.stderr)
        sys.exit(1)

    try:
        conn = psycopg2.connect(postgres_url)
    except Exception as e:
        print(f"Cannot connect to PostgreSQL at {url.hostname}:{url.port}. Is PostgreSQL running?", file=sys.stderr)
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    try:
        cur.execute(f'CREATE DATABASE "{db_name}";')
        print(f'Database "{db_name}" created successfully.')
    except psycopg2.errors.DuplicateDatabase:
        print(f'Database "{db_name}" already exists.')
    except Exception as e:
        print(f"Failed to create database: {e}", file=sys.stderr)
        cur.close()
        conn.close()
        sys.exit(1)

    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
