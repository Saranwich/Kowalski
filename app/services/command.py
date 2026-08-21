from app.clients import line
from app.services import task

HELP_TEXT = "\n".join([
    "คำสั่งที่ใช้ได้",
    "/add_task เรื่อง | รายละเอียด | กำหนดส่ง",
    "/list_task - ดูการบ้านที่ค้าง (ใส่ all ต่อท้ายเพื่อดูที่ทำเสร็จแล้วด้วย)",
    "/edit_task เลขที่ | เรื่องใหม่ | รายละเอียดใหม่ | กำหนดส่งใหม่",
    "   (ช่องไหนไม่อยากแก้ เว้นว่างไว้ได้ เช่น /edit_task 3 | | | 2026-10-01)",
    "/done_task เลขที่ - ปิดงานที่ทำเสร็จแล้ว",
    "/del_task เลขที่ - ลบทิ้ง",
    "/help - ดูคำสั่งทั้งหมด",
    "",
    "ทุกคำสั่งต้องมี / นำหน้าเสมอ ไม่งั้นผมจะตอบเป็นข้อความธรรมดาครับ",
])

async def help_command (line_user_id, reply_token, *_):
    await line.replies_message(reply_token, HELP_TEXT)
    return 0

command_map = {
    "/add_task":task.add_task,
    "/list_task":task.list_tasks,
    "/edit_task":task.edit_task,
    "/done_task":task.done_task,
    "/del_task":task.del_task,
    "/help":help_command
}

async def do_command(line_user_id, reply_token, input_command: str):
    params = input_command.split(" ",1) # [/command] or [/command, param1, ...]
    command = command_map.get(f"{params[0]}")
    if command is None:
        await line.replies_message(reply_token, f"ไม่รู้จักคำสั่ง {params[0]} ครับ\n\n{HELP_TEXT}")
        return
    if len(params) >= 2 :
        args = [a.strip() for a in params[1].split("|", 3)]
        await command(line_user_id, reply_token, *args)
    else :
        await command(line_user_id, reply_token)
    return
