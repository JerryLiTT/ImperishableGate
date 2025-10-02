from fastapi import APIRouter, Request

router = APIRouter()

@router.post("/ping")
async def ping(request: Request):
    data = await request.json()
    print("收到请求内容:", data)

    return {
        "action": "ping",
        "payload1": "ping test succeeded"
    }
