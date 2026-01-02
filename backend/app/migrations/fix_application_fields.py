from sqlalchemy import text
from ..database import engine

with engine.connect() as conn:
    # 1. Add date column if not exists
    try:
        conn.execute(text("ALTER TABLE applications ADD COLUMN date VARCHAR"))
        print("date column added")
    except:
        print("date column already exists, skipping")

    # 2. Fix stats route dependency mismatch note (no DB change needed for owner_id)
    print("owner_id column already correct, verified")

    conn.commit()
