"""
One-off migration: splits the old monolithic ad_execution table (which stored
generated video production content directly) into the new lightweight
ad_execution "recipe" table plus a new video_creative_execution table holding
the previously-generated content. Run once against app.db.
"""

import json
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "app.db"

DEFAULT_CREATIVE_TYPE = "video"
DEFAULT_PLATFORM = "Meta Ads"
DEFAULT_FORMAT = "Vertical Video 9:16"
DEFAULT_DURATION_SECONDS = 15


def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        "SELECT id, creative_strategy_id, name, hook_strategy, structure, scenes, "
        "asset_requirements, production_notes, cta, created_at, updated_at FROM ad_execution"
    )
    old_rows = cur.fetchall()
    print(f"Found {len(old_rows)} existing ad_execution rows")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS video_creative_execution (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ad_execution_id INTEGER NOT NULL REFERENCES ad_execution(id) ON DELETE CASCADE,
            duration_seconds INTEGER,
            hook_strategy JSON,
            structure JSON,
            scenes JSON,
            asset_requirements JSON,
            production_notes JSON,
            cta JSON,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    for row in old_rows:
        (ad_execution_id, _csi, _name, hook_strategy, structure, scenes,
         asset_requirements, production_notes, cta, created_at, updated_at) = row

        cur.execute(
            """
            INSERT INTO video_creative_execution
                (ad_execution_id, duration_seconds, hook_strategy, structure,
                 scenes, asset_requirements, production_notes, cta, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                ad_execution_id,
                DEFAULT_DURATION_SECONDS,
                hook_strategy,
                structure,
                scenes,
                asset_requirements,
                production_notes,
                cta,
                created_at,
                updated_at,
            ),
        )

    print(f"Inserted {len(old_rows)} video_creative_execution rows")

    cur.execute("""
        CREATE TABLE ad_execution_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            creative_strategy_id INTEGER NOT NULL REFERENCES creative_strategy(id) ON DELETE CASCADE,
            name VARCHAR,
            creative_type VARCHAR NOT NULL,
            platform VARCHAR,
            format VARCHAR,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    for row in old_rows:
        (ad_execution_id, creative_strategy_id, name, *_rest, created_at, updated_at) = row

        cur.execute(
            """
            INSERT INTO ad_execution_new
                (id, creative_strategy_id, name, creative_type, platform, format, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                ad_execution_id,
                creative_strategy_id,
                name,
                DEFAULT_CREATIVE_TYPE,
                DEFAULT_PLATFORM,
                DEFAULT_FORMAT,
                created_at,
                updated_at,
            ),
        )

    cur.execute("DROP TABLE ad_execution")
    cur.execute("ALTER TABLE ad_execution_new RENAME TO ad_execution")

    conn.commit()

    cur.execute("SELECT count(*) FROM ad_execution")
    print(f"ad_execution now has {cur.fetchone()[0]} rows")
    cur.execute("SELECT count(*) FROM video_creative_execution")
    print(f"video_creative_execution now has {cur.fetchone()[0]} rows")

    conn.close()


if __name__ == "__main__":
    main()
