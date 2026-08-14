import httpx
from app.core.config import LINE_CHANNEL_ACCESS_TOKEN, LINE_CHANNEL_SECRET

async def replies_message (reply_token, text):
    print(f"reply token: {reply_token}\ntext: {text}")

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            url="https://api.line.me/v2/bot/message/reply",
            headers= {"Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"},
            json={"replyToken": reply_token,
                "messages":[
                    {"type": "text", "text" : "you said"},
                    {"type": "text", "text" : text}
                    ]
                }
            )
    print(f"status code: {resp.status_code}")
    for evnet in resp.json():
        print(evnet,": ", resp.json()[evnet],end="\n\n")
    return resp