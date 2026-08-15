from app.core.config import TYPHOON_API_KEY,TYPHOON_BASE_URL
from httpx import AsyncClient
from traceback import print_exc

async def chat (messages: list[dict]) -> str:
    async with AsyncClient() as client:
        try:
            resp = await client.post(
                url= TYPHOON_BASE_URL + "/chat/completions",
                headers={"Authorization" : f"Bearer {TYPHOON_API_KEY}"},
                json={
                    "model": "typhoon-v2.5-30b-a3b-instruct",
                    "messages": messages,
                    "temperature": 0.3,
                    "max_completion_tokens" : 512,
                    "top_p":0.7,
                    "frequency_penalty": 0,
                    "stream": False
                },
                timeout=30
            )

            if resp.status_code != 200:
                return f"system: status code {resp.status_code}"
            
            resp_ans : str = resp.json()["choices"][0]["message"]["content"]
            return resp_ans
        except Exception as e:
            print_exc()
            return f"system fail : {type(e).__name__}"