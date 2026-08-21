from app.services import task

command_map = {
    "/add_task":task.add_task
}

def do_command(line_user_id, input_command: str):
    params = input_command.split(" ",1) # [/command] or [/command, param1, ...]
    command = command_map.get(f"{params[0]}")
    if command is None:
        return
    if len(params) >= 2 : 
        args = [a.strip() for a in params[1].split("|")]
        command(line_user_id,*(args))
    return

