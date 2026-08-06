from sqlalchemy import inspect, text
from .db import Base, engine
from domain.models import models

def init_db():
    Base.metadata.create_all(bind=engine)
    _add_missing_favorite_columns()

def _add_missing_favorite_columns():
    """Additive migration: adds `is_favorite` to tables that already existed
    before this column was introduced (create_all only creates missing
    tables, it never alters existing ones)."""
    inspector = inspect(engine)
    existing_tables = set(inspector.get_table_names())

    for table in Base.metadata.tables.values():
        if table.name not in existing_tables:
            continue

        columns = {c["name"] for c in inspector.get_columns(table.name)}
        if "is_favorite" not in columns:
            with engine.begin() as conn:
                conn.execute(
                    text(f'ALTER TABLE "{table.name}" ADD COLUMN is_favorite BOOLEAN NOT NULL DEFAULT 0')
                )