from app.clients import line, typhoon
from app.core.config import KOWALSKI_SYSTEM_PROMPT

async def replies_line_with_typhoon(reply_token, text):
    messages = [
                {"role": "system", "content": KOWALSKI_SYSTEM_PROMPT},
                {"role": "user", "content": text},
            ]
    resp = await typhoon.chat(messages)
    line_reply_resp = await line.replies_message(reply_token, resp)
