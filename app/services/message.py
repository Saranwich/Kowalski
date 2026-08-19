from app.clients import line, typhoon
from app.core.config import KOWALSKI_SYSTEM_PROMPT
from app.database import db

async def replies_line_with_typhoon(line_user_id: str, reply_token: str, text: str):

    db.save_message(line_user_id, "user", text)
    rct_con = db.get_recent_messages_by_lineid(line_user_id = line_user_id, limit=15)
    messages = [{"role": "system", "content": KOWALSKI_SYSTEM_PROMPT}] + rct_con
    resp = await typhoon.chat(messages)
    await line.replies_message(reply_token, resp)
    db.save_message(line_user_id, "assistant", resp)
