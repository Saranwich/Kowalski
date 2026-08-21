from fastapi import APIRouter, Request, HTTPException, BackgroundTasks
from app.services import message, auth, command
import traceback
import json

router = APIRouter()

@router.post("/api/webhook")
async def webhook(request: Request, bg_task: BackgroundTasks):
    header = dict(request.headers)
    sig = header.get("x-line-signature")
    if sig is None : 
        print("header-x-line-signature not found ")
        raise HTTPException(status_code=400)
    raw_body = await request.body()
    if not auth.is_valid_line_signature(raw_body,sig) : 
        print("not valid signature")
        raise HTTPException(status_code=400)
    try :
        body = json.loads(raw_body)

        print(raw_body,end="\n\n--------------\n\n")

        # verify - line signature

        events = body["events"]
        for event in events:
            if (event["type"] == "message") :

                # text message
                if (event["message"]["type"] == "text" ) :

                    if (event["message"]["text"] == ""):
                        continue

                    if event["message"]["text"][0] == "/":
                        bg_task.add_task(command.do_command, event["source"]["userId"], event["replyToken"], event["message"]["text"])

                    #go to message services
                    else : 
                        bg_task.add_task(message.replies_line_with_typhoon, event["source"]["userId"], event["replyToken"], event["message"]["text"])

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
    return {}
