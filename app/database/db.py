import sqlite3, datetime
from app.core.config import DB_PATH


def init_db():
    conn:sqlite3.Connection = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id      INTEGER PRIMARY KEY,
            line_user_id TEXT,
            role    TEXT NOT NULL,
            content  TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_message(line_user_id:str, role : str, content: str):
    conn:sqlite3.Connection = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO messages (line_user_id, role, content, created_at) VALUES (?,?,?,?)",
        (
            line_user_id,
            role,
            content,
            _get_time()
        ))
    conn.commit()
    conn.close()

def get_recent_messages_by_lineid (line_user_id, limit: int = 5):
    with sqlite3.connect(DB_PATH) as conn:
        dt = conn.execute(
            "SELECT role, content FROM messages WHERE line_user_id = ? ORDER BY id DESC LIMIT ?",
            (line_user_id, limit)
            ).fetchall()
    conn.close()
    messages = []
    for row in dt[::-1]:
        messages.append(dict({"role":row[0], "content":row[1]}))
    return messages

def _get_time ():
    dt =  datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
    return dt