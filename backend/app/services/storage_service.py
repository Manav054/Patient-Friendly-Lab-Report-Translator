import json
import sqlite3
import uuid
from pathlib import Path

# Define the base directory for data storage
BASE_DIR = Path(__file__).resolve().parent.parent.parent / "data"
DB_PATH = BASE_DIR / "reports.db"


def _ensure_db():
    if not BASE_DIR.exists():
        BASE_DIR.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        # Check if table exists
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='reports'"
        )
        table_exists = cursor.fetchone()

        if not table_exists:
            cursor.execute("""
                CREATE TABLE reports (
                    id TEXT PRIMARY KEY,
                    patient_id TEXT,
                    payload TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        else:
            # Check for patient_id column
            cursor.execute("PRAGMA table_info(reports)")
            columns = [col[1] for col in cursor.fetchall()]
            if "patient_id" not in columns:
                cursor.execute("ALTER TABLE reports ADD COLUMN patient_id TEXT")
            if "created_at" not in columns:
                cursor.execute("ALTER TABLE reports ADD COLUMN created_at TIMESTAMP")

        conn.commit()


def save_report(data: dict, patient_id: str = None) -> str:
    """
    Saves a lab report JSON payload to the SQLite database.
    Returns the generated UUID string.
    """
    _ensure_db()
    report_id = str(uuid.uuid4())

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO reports (id, patient_id, payload, created_at) VALUES (?, ?, ?, CURRENT_TIMESTAMP)",
            (report_id, patient_id, json.dumps(data, ensure_ascii=False)),
        )
        conn.commit()

    return report_id


def get_report(report_id: str) -> dict | None:
    """
    Retrieves a lab report JSON payload by its UUID from SQLite.
    Returns None if not found.
    """
    _ensure_db()

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT payload FROM reports WHERE id = ?", (report_id,))
        row = cursor.fetchone()

    if row:
        try:
            return json.loads(row[0])
        except json.JSONDecodeError:
            return None
    return None


def get_patient_reports(patient_id: str) -> list[dict]:
    """
    Retrieves all historical reports for a given patient, ordered chronologically by created_at.
    """
    _ensure_db()

    reports = []
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, created_at, payload FROM reports WHERE patient_id = ? ORDER BY created_at ASC",
            (patient_id,),
        )
        rows = cursor.fetchall()

        for row in rows:
            try:
                data = json.loads(row[2])
                data["report_id"] = row[0]
                data["created_at"] = row[1]
                reports.append(data)
            except json.JSONDecodeError:
                continue

    return reports
