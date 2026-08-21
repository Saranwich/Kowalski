from app.clients import line
from app.database import db

async def add_task (line_user_id, reply_token, task_title:str = "untitle", desc:str = "desc", due_to:str = "2026-12-31 23:59", noti = True):
    db.save_task(line_user_id, task_title, desc, due_to, noti)
    db.save_message(line_user_id, "system", f"{line_user_id} added task {task_title} -- {desc}, due to: {due_to}, noti: {noti} ")
    await line.replies_message(reply_token, f"จดให้แล้วครับ\n{task_title}\n{desc}\nกำหนดส่ง {due_to}")
    return 0
