import sqlite3
from datetime import datetime, timezone


class JobStore:
    def __init__(self, path: str = "jobs.db"):
        self.conn = sqlite3.connect(path)
        self.conn.execute(
            """CREATE TABLE IF NOT EXISTS seen_jobs (
                id TEXT PRIMARY KEY,
                title TEXT, company TEXT, url TEXT, source TEXT,
                first_seen TEXT
            )"""
        )

    def is_new(self, job_id: str) -> bool:
        row = self.conn.execute("SELECT 1 FROM seen_jobs WHERE id = ?", (job_id,)).fetchone()
        return row is None

    def mark_seen(self, job) -> None:
        self.conn.execute(
            "INSERT OR IGNORE INTO seen_jobs VALUES (?, ?, ?, ?, ?, ?)",
            (job.id, job.title, job.company, job.url, job.source,
             datetime.now(timezone.utc).isoformat()),
        )
        self.conn.commit()
