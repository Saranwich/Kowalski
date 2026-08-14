from app.clients import line

async def replies(reply_token, text):
    line_reply_resp = await line.replies_message(reply_token, text)
