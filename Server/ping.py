from fastapi import APIRouter, Request

'''
gate "127.0.0.1:9323" ping "www.github.com"                                                                                
{'server': '100.92.189.86:9323', 'action': 'ping', 'payload1': 'www.github.com'}

'''

router = APIRouter()

@router.post("/ping")
async def ping(request: Request):
    data = await request.json()
    print("收到请求内容:", data)

    return {
        "action": "ping",
        "payload1": "ping test succeeded"
    }
