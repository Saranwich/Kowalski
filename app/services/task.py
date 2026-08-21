from app.clients import line
from app.database import db

async def add_task (line_user_id, reply_token, task_title:str = "untitle", desc:str = "desc", due_to:str = "2026-12-31 23:59", *_):
    db.save_task(line_user_id, task_title, desc, due_to, True)
    db.save_message(line_user_id, "system", f"{line_user_id} added task {task_title} -- {desc}, due to: {due_to}")
    await line.replies_message(reply_token, f"จดให้แล้วครับ\n{task_title}\n{desc}\nกำหนดส่ง {due_to}")
    return 0

async def edit_task (line_user_id, reply_token, task_id:str = "", task_title:str = "", desc:str = "", due_to:str = "", *_):
    if not task_id.isdigit():
        await line.replies_message(reply_token, "ใส่เลขที่ด้วยครับ เช่น\n/edit_task 3 | เรื่องใหม่ | รายละเอียดใหม่ | 2026-10-01")
        return 0

    # ช่องไหนเว้นว่างไว้ = เก็บของเดิม เลยต้องอ่านแถวปัจจุบันมาก่อน
    current = None
    for t in db.get_tasks_by_lineid(line_user_id, include_done=True):
        if t["id"] == int(task_id):
            current = t
            break
    if current is None:
        await line.replies_message(reply_token, f"ไม่เจอการบ้านข้อ {task_id} ครับ")
        return 0

    new_title = task_title or current["title"]
    new_desc = desc or current["desc"]
    new_due_to = due_to or current["due_to"]
    db.update_task(line_user_id, int(task_id), new_title, new_desc, new_due_to)
    db.save_message(line_user_id, "system", f"{line_user_id} edited task id {task_id} -- {new_title} -- {new_desc}, due to: {new_due_to}")
    await line.replies_message(reply_token, f"แก้ให้แล้วครับ\n#{task_id} {new_title}\n{new_desc}\nกำหนดส่ง {new_due_to}")
    return 0

async def list_tasks (line_user_id, reply_token, mode:str = "", *_):
    include_done = mode.lower() == "all"
    tasks = db.get_tasks_by_lineid(line_user_id, include_done)
    if not tasks:
        await line.replies_message(reply_token, "ยังไม่มีการบ้านค้างอยู่ครับ")
        return 0

    rows = ["การบ้านทั้งหมด" if include_done else "การบ้านที่ยังค้างอยู่"]
    for t in tasks:
        mark = "[เสร็จแล้ว] " if t["done"] else ""
        rows.append("")
        rows.append(f"#{t['id']} {mark}{t['title']}")
        rows.append(f"   {t['desc']}")
        rows.append(f"   ส่ง {t['due_to']}")
    rows.append("")
    rows.append("ใช้เลขหลัง # กับ /done_task /del_task /edit_task ได้เลยครับ")
    await line.replies_message(reply_token, "\n".join(rows))
    return 0

async def done_task (line_user_id, reply_token, task_id:str = "", *_):
    if not task_id.isdigit():
        await line.replies_message(reply_token, "ใส่เลขที่ด้วยครับ เช่น /done_task 3")
        return 0

    changed = db.mark_task_done(line_user_id, int(task_id))
    if changed == 0:
        await line.replies_message(reply_token, f"ไม่เจอการบ้านข้อ {task_id} ครับ")
        return 0

    db.save_message(line_user_id, "system", f"{line_user_id} finished task id {task_id}")
    await line.replies_message(reply_token, f"ปิดข้อ {task_id} ให้แล้วครับ")
    return 0

async def del_task (line_user_id, reply_token, task_id:str = "", *_):
    if not task_id.isdigit():
        await line.replies_message(reply_token, "ใส่เลขที่ด้วยครับ เช่น /del_task 3")
        return 0

    changed = db.delete_task(line_user_id, int(task_id))
    if changed == 0:
        await line.replies_message(reply_token, f"ไม่เจอการบ้านข้อ {task_id} ครับ")
        return 0

    db.save_message(line_user_id, "system", f"{line_user_id} deleted task id {task_id}")
    await line.replies_message(reply_token, f"ลบข้อ {task_id} ทิ้งแล้วครับ")
    return 0
