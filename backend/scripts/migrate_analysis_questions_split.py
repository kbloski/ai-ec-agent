"""
One-off migration: splits the old monolithic analysis_questions table (which
stored the question/answer content directly alongside the analysis link) into
a new question_answers content table plus a lightweight analysis_questions
link table (analysis_id, question_answer_id). Run once against app.db.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "app.db"


def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        "SELECT id, analysis_id, question, answer, score, confidence, created_at "
        "FROM analysis_questions"
    )
    old_rows = cur.fetchall()
    print(f"Found {len(old_rows)} existing analysis_questions rows")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS question_answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT,
            score INTEGER,
            confidence FLOAT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    for row in old_rows:
        (id_, _analysis_id, question, answer, score, confidence, created_at) = row

        cur.execute(
            """
            INSERT INTO question_answers
                (id, question, answer, score, confidence, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (id_, question, answer, score, confidence, created_at),
        )

    print(f"Inserted {len(old_rows)} question_answers rows")

    cur.execute("""
        CREATE TABLE analysis_questions_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            analysis_id INTEGER NOT NULL REFERENCES analysis(id) ON DELETE CASCADE,
            question_answer_id INTEGER NOT NULL REFERENCES question_answers(id) ON DELETE CASCADE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    for row in old_rows:
        (id_, analysis_id, _question, _answer, _score, _confidence, created_at) = row

        cur.execute(
            """
            INSERT INTO analysis_questions_new
                (id, analysis_id, question_answer_id, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (id_, analysis_id, id_, created_at),
        )

    cur.execute("DROP TABLE analysis_questions")
    cur.execute("ALTER TABLE analysis_questions_new RENAME TO analysis_questions")

    conn.commit()

    cur.execute("SELECT count(*) FROM question_answers")
    print(f"question_answers now has {cur.fetchone()[0]} rows")
    cur.execute("SELECT count(*) FROM analysis_questions")
    print(f"analysis_questions now has {cur.fetchone()[0]} rows")

    conn.close()


if __name__ == "__main__":
    main()
