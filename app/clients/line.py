import httpx
from traceback import print_exc
from app.core.config import LINE_CHANNEL_ACCESS_TOKEN, LINE_CHANNEL_SECRET

async def replies_message (reply_token, text):
    print(f"reply token: {reply_token}\ntext: {text}")
    try:
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
        for event in resp.json():
            print(event,": ", resp.json()[event],end="\n\n")
        return resp
    
    except Exception as e:
        print(f"error: {e}")
        print_exc()
        return None