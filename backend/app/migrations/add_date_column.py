from sqlalchemy import text
from ..database import engine

with engine.connect() as conn:
    conn.execute(text("ALTER TABLE applications ADD COLUMN date VARCHAR"))
    conn.commit()
    print("Migration: 'date' column added")
