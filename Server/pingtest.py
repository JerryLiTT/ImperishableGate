from fastapi import APIRouter, Request
from datetime import datetime

router = APIRouter()

@router.post("/pingtest")
async def pingtest(request: Request):
    data = await request.json()
    print("收到请求内容:", data)

    # 把输入内容转为字符串再重复两次
    repeated = str(data["payload1"]) * 2

    # 获取当前时间
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {
        "action": "pingtest",
        "payload1": repeated,
        "time": now
    }
