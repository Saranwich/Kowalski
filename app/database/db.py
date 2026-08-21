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
        )""")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id      INTEGER PRIMARY KEY,
            line_user_id TEXT,
            title    TEXT NOT NULL,
            desc  TEXT,
            due_to TEXT,
            noti BOOL NOT NULL,
            done INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL
        )
    """)
    # ตาราง tasks ที่สร้างไว้ก่อนหน้านี้ยังไม่มี column done — CREATE TABLE IF NOT EXISTS ข้ามให้เฉยๆ
    cols = [row[1] for row in conn.execute("PRAGMA table_info(tasks)")]
    if "done" not in cols:
        conn.execute("ALTER TABLE tasks ADD COLUMN done INTEGER NOT NULL DEFAULT 0")
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

def save_task(line_user_id:str, title:str, desc:str, due_to, noti:bool = True):
    conn:sqlite3.Connection = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO tasks (line_user_id, title, desc, due_to, noti, created_at) VALUES (?,?,?,?,?,?)",
        (
            line_user_id,
            title,
            desc,
            due_to,
            noti,
            _get_time()
        ))
    conn.commit()
    conn.close()

def get_tasks_by_lineid (line_user_id, include_done: bool = False):
    sql = "SELECT id, title, desc, due_to, done FROM tasks WHERE line_user_id = ?"
    if not include_done:
        sql += " AND done = 0"
    sql += " ORDER BY due_to, id"
    with sqlite3.connect(DB_PATH) as conn:
        dt = conn.execute(sql, (line_user_id,)).fetchall()
    conn.close()
    tasks = []
    for row in dt:
        tasks.append({"id":row[0], "title":row[1], "desc":row[2], "due_to":row[3], "done":row[4]})
    return tasks

def mark_task_done (line_user_id, task_id: int):
    conn:sqlite3.Connection = sqlite3.connect(DB_PATH)
    # line_user_id อยู่ใน WHERE ด้วย เพื่อไม่ให้ใครไปปิดงานของคนอื่นด้วยการเดาเลข id
    cur = conn.execute(
        "UPDATE tasks SET done = 1 WHERE id = ? AND line_user_id = ?",
        (task_id, line_user_id))
    changed = cur.rowcount
    conn.commit()
    conn.close()
    return changed

def update_task (line_user_id, task_id: int, title:str, desc:str, due_to):
    conn:sqlite3.Connection = sqlite3.connect(DB_PATH)
    cur = conn.execute(
        "UPDATE tasks SET title = ?, desc = ?, due_to = ? WHERE id = ? AND line_user_id = ?",
        (title, desc, due_to, task_id, line_user_id))
    changed = cur.rowcount
    conn.commit()
    conn.close()
    return changed

def delete_task (line_user_id, task_id: int):
    conn:sqlite3.Connection = sqlite3.connect(DB_PATH)
    cur = conn.execute(
        "DELETE FROM tasks WHERE id = ? AND line_user_id = ?",
        (task_id, line_user_id))
    changed = cur.rowcount
    conn.commit()
    conn.close()
    return changed

def _get_time ():
    dt =  datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
    return dt