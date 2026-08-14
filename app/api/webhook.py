from fastapi import APIRouter, Request
from app.services import message
import traceback
router = APIRouter()

@router.post("/api/webhook")
async def webhook(request: Request):
    try :
        body = await request.json()
        events = body["events"]
        for event in events:
            if (event["type"] == "message") :

                # text message
                if (event["message"]["type"] == "text" ) :
                    #go to message services
                    await message.replies(event["replyToken"], event["message"]["text"])
                # sticker message
                elif (event["message"]["type"] == "sticker" ):
                    print(event)

                # images message
                elif (event["message"]["type"] == "image"):
                    print(event)

                # images message
                elif (event["message"]["type"] == "video"):
                    print(event)

                # other message type
                else :
                    print("Not valid message type")
                    print(f"\n\n {event} \n\n")

            #other event
            else :
                print(f"not valid event type")
        
    except Exception as e:
        print(f"something went wrong {e}")
        traceback.print_exc()
        
    return {}
