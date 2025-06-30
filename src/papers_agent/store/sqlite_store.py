from __future__ import annotations
import sqlite3, json, pathlib

DB_PATH = pathlib.Path("data/app/clinical.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

DDL = """
CREATE TABLE IF NOT EXISTS trials(
  pmid TEXT PRIMARY KEY,
  title TEXT,
  sample_size INTEGER,
  arms TEXT,             
  primary_outcome TEXT,
  abstract TEXT,
  pub_date TEXT           
);
"""

def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute(DDL)
    return conn

def upsert_trial(rec: dict):
    with get_conn() as conn:
        conn.execute(
            """INSERT INTO trials
               (pmid, title, sample_size, arms, primary_outcome, abstract, pub_date)
               VALUES (:pmid, :title, :sample_size, :arms, :primary_outcome, :abstract, :pub_date)
               ON CONFLICT(pmid) DO UPDATE SET
                   title=excluded.title,
                   sample_size=excluded.sample_size,
                   arms=excluded.arms,
                   primary_outcome=excluded.primary_outcome,
                   abstract=excluded.abstract,
                   pub_date=excluded.pub_date;
            """,
            {**rec, "arms": json.dumps(rec["arms"])},
        )

def recent_trials(days: int = 7) -> list[dict]:
    with get_conn() as conn:
        cur = conn.execute(
            """
            SELECT pmid, title, sample_size, arms, primary_outcome, abstract
            FROM trials
            WHERE julianday('now') - julianday(pub_date) <= ?
            ORDER BY pub_date DESC;
            """,
            (days,),
        )
        rows = [
            dict(
                pmid=r[0],
                title=r[1],
                sample_size=r[2],
                arms=json.loads(r[3]),
                primary_outcome=r[4],
                abstract=r[5],
            )
            for r in cur.fetchall()
        ]
    return rows
