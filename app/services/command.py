from app.clients import line
from app.services import task

command_map = {
    "/add_task":task.add_task
}

async def do_command(line_user_id, reply_token, input_command: str):
    params = input_command.split(" ",1) # [/command] or [/command, param1, ...]
    command = command_map.get(f"{params[0]}")
    if command is None:
        await line.replies_message(reply_token, f"ไม่รู้จักคำสั่ง {params[0]} ครับ")
        return
    if len(params) >= 2 :
        args = [a.strip() for a in params[1].split("|", 2)]
        await command(line_user_id, reply_token, *args)
    else :
        await command(line_user_id, reply_token)
    return
